"""
AI Service for EclipseLink AI
Handles OpenAI Whisper (transcription) and Anthropic Claude (SBAR generation)

Includes mock responses when API keys are not configured.
"""
import asyncio
import logging
from typing import Optional, Dict, Any
from app.config import settings

logger = logging.getLogger(__name__)


class AIService:
    """
    AI Service with automatic fallback to mocks when API keys not configured
    """

    def __init__(self):
        self.has_whisper = bool(settings.OPENAI_API_KEY and settings.OPENAI_API_KEY != "your-openai-api-key-here")
        self.has_claude = bool(settings.ANTHROPIC_API_KEY and settings.ANTHROPIC_API_KEY != "your-anthropic-api-key-here")

        if self.has_whisper:
            from openai import AsyncOpenAI
            self.openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            logger.info("✓ OpenAI Whisper API configured")
        else:
            logger.warning("⚠️  OpenAI API key not configured - using MOCK transcription")

        if self.has_claude:
            from anthropic import AsyncAnthropic
            self.anthropic_client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
            logger.info("✓ Anthropic Claude API configured")
        else:
            logger.warning("⚠️  Anthropic API key not configured - using MOCK SBAR generation")

    async def transcribe_audio(self, audio_file_path: str) -> Dict[str, Any]:
        """
        Transcribe audio using OpenAI Whisper API or mock

        Returns:
            {
                "text": "transcribed text...",
                "confidence": 0.95,
                "duration_seconds": 45,
                "is_mock": False
            }
        """
        if self.has_whisper:
            return await self._transcribe_with_whisper(audio_file_path)
        else:
            return await self._transcribe_mock(audio_file_path)

    async def _transcribe_with_whisper(self, audio_file_path: str) -> Dict[str, Any]:
        """Real OpenAI Whisper transcription"""
        try:
            with open(audio_file_path, "rb") as audio_file:
                response = await self.openai_client.audio.transcriptions.create(
                    model=settings.OPENAI_WHISPER_MODEL,
                    file=audio_file,
                    response_format="verbose_json"
                )

            return {
                "text": response.text,
                "confidence": 0.95,  # Whisper doesn't return confidence, estimate high
                "duration_seconds": int(response.duration) if hasattr(response, 'duration') else None,
                "is_mock": False
            }
        except Exception as e:
            logger.error(f"Whisper API error: {e}")
            # Fallback to mock on error
            return await self._transcribe_mock(audio_file_path)

    async def _transcribe_mock(self, audio_file_path: str) -> Dict[str, Any]:
        """Mock transcription for development"""
        await asyncio.sleep(2)  # Simulate API delay

        mock_transcript = """
        Patient is Sarah Johnson, 67-year-old female in room 302.
        Admitted yesterday for pneumonia. Currently on IV antibiotics, ceftriaxone 2 grams every 12 hours.
        Vitals are stable - BP 128/76, heart rate 82, temp 98.6, oxygen saturation 94% on 2 liters nasal cannula.
        She's been coughing less today and reports feeling better.
        Pain level is 2 out of 10. She's eating well and ambulating with assistance.
        No allergies. Full code status. Family visited this morning.
        Plan is to continue antibiotics for 48 more hours, then reassess for discharge.
        """

        return {
            "text": mock_transcript.strip(),
            "confidence": 0.92,
            "duration_seconds": 45,
            "is_mock": True
        }

    async def generate_sbar(
        self,
        transcript: str,
        patient_context: Optional[Dict[str, Any]] = None,
        user_role: str = "RN",
        is_baseline: bool = True
    ) -> Dict[str, Any]:
        """
        Generate SBAR using Anthropic Claude or mock

        Args:
            transcript: Voice transcription text
            patient_context: Patient info (name, age, diagnosis, etc.)
            user_role: Clinical role (RN, MD, PT, etc.) for customization
            is_baseline: Is this the first handoff or an update?

        Returns:
            {
                "situation": "...",
                "background": "...",
                "assessment": "...",
                "recommendation": "...",
                "processing_time_ms": 5234,
                "is_mock": False
            }
        """
        if self.has_claude:
            return await self._generate_sbar_with_claude(transcript, patient_context, user_role, is_baseline)
        else:
            return await self._generate_sbar_mock(transcript, patient_context, user_role, is_baseline)

    async def _generate_sbar_with_claude(
        self,
        transcript: str,
        patient_context: Optional[Dict[str, Any]],
        user_role: str,
        is_baseline: bool
    ) -> Dict[str, Any]:
        """Real Anthropic Claude SBAR generation"""
        import time
        start_time = time.time()

        try:
            prompt = self._build_sbar_prompt(transcript, patient_context, user_role, is_baseline)

            response = await self.anthropic_client.messages.create(
                model=settings.ANTHROPIC_MODEL,
                max_tokens=settings.ANTHROPIC_MAX_TOKENS,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            # Parse SBAR from response
            sbar_text = response.content[0].text
            sbar = self._parse_sbar_response(sbar_text)

            processing_time_ms = int((time.time() - start_time) * 1000)

            return {
                **sbar,
                "processing_time_ms": processing_time_ms,
                "is_mock": False
            }
        except Exception as e:
            logger.error(f"Claude API error: {e}")
            # Fallback to mock on error
            return await self._generate_sbar_mock(transcript, patient_context, user_role, is_baseline)

    async def _generate_sbar_mock(
        self,
        transcript: str,
        patient_context: Optional[Dict[str, Any]],
        user_role: str,
        is_baseline: bool
    ) -> Dict[str, Any]:
        """Mock SBAR generation for development"""
        await asyncio.sleep(3)  # Simulate API delay

        patient_name = patient_context.get("name", "Sarah Johnson") if patient_context else "Sarah Johnson"
        patient_age = patient_context.get("age", 67) if patient_context else 67

        sbar = {
            "situation": f"{patient_name}, {patient_age}-year-old female in Room 302, admitted for pneumonia. Currently stable on IV antibiotics (ceftriaxone 2g q12h).",

            "background": f"Admitted 24 hours ago with productive cough, fever (101.2°F), and shortness of breath. History of hypertension, well-controlled. No drug allergies. Full code status.",

            "assessment": "Patient showing improvement - temperature normalized (98.6°F), cough decreasing, O2 sat 94% on 2L NC. Vital signs stable (BP 128/76, HR 82). Pain minimal (2/10). Tolerating diet, ambulating with assist. No respiratory distress at rest.",

            "recommendation": "Continue current antibiotic regimen for 48 hours. Monitor respiratory status q4h. Wean oxygen as tolerated with goal of room air. Physical therapy consult for mobility. Reassess for discharge in 2 days if continued improvement. Family education on home care completed."
        }

        return {
            **sbar,
            "processing_time_ms": 3000,
            "is_mock": True
        }

    def _build_sbar_prompt(self, transcript: str, patient_context: Optional[Dict], user_role: str, is_baseline: bool) -> str:
        """Build prompt for Claude"""
        handoff_type = "initial baseline handoff" if is_baseline else "handoff update"

        prompt = f"""You are an expert clinical documentation assistant helping a {user_role} create a structured SBAR (Situation, Background, Assessment, Recommendation) handoff note.

Given this voice transcription from a {handoff_type}:

{transcript}

Generate a professional, concise SBAR using this exact format:

SITUATION:
[1-2 sentences: Patient identity, location, primary reason for care]

BACKGROUND:
[2-3 sentences: Relevant history, admission reason, significant medical history, allergies, code status]

ASSESSMENT:
[2-4 sentences: Current condition, vital signs, key observations, response to treatment]

RECOMMENDATION:
[2-3 sentences: Plan of care, monitoring needs, follow-up actions]

Important:
- Be concise and clinically relevant
- Focus on information a {user_role} would prioritize
- Use medical terminology appropriately
- Include specific vital signs and medications when mentioned
- Highlight any changes or concerns"""

        return prompt

    def _parse_sbar_response(self, sbar_text: str) -> Dict[str, str]:
        """Parse SBAR sections from Claude response"""
        sections = {"situation": "", "background": "", "assessment": "", "recommendation": ""}

        current_section = None
        for line in sbar_text.split("\n"):
            line = line.strip()
            if line.upper().startswith("SITUATION:"):
                current_section = "situation"
                line = line[10:].strip()
            elif line.upper().startswith("BACKGROUND:"):
                current_section = "background"
                line = line[11:].strip()
            elif line.upper().startswith("ASSESSMENT:"):
                current_section = "assessment"
                line = line[11:].strip()
            elif line.upper().startswith("RECOMMENDATION:"):
                current_section = "recommendation"
                line = line[15:].strip()

            if current_section and line:
                sections[current_section] += line + " "

        # Clean up
        return {k: v.strip() for k, v in sections.items()}

    async def detect_critical_alerts(self, transcript: str, sbar: Dict[str, str]) -> Optional[Dict[str, Any]]:
        """
        Detect critical alerts from transcript/SBAR (3-layer approach)

        Returns None if no alert, or:
            {
                "alert_type": "sepsis_risk",
                "severity": "critical",
                "confidence": 0.89,
                "message": "Patient shows signs of sepsis...",
                "recommended_actions": "Notify physician immediately..."
            }
        """
        # Simple keyword-based detection for MVP
        # In production, would use Claude to analyze for clinical deterioration

        combined_text = f"{transcript} {sbar.get('situation','')} {sbar.get('assessment','')}".lower()

        critical_keywords = {
            "sepsis_risk": ["sepsis", "septic", "fever", "infection", "hypotension"],
            "cardiac_event": ["chest pain", "mi", "heart attack", "cardiac arrest"],
            "respiratory_distress": ["respiratory distress", "cannot breathe", "hypoxia", "desaturation"],
            "fall_risk": ["fell", "fall", "unsteady", "dizzy"],
            "stroke_symptoms": ["stroke", "facial droop", "slurred speech", "weakness"]
        }

        for alert_type, keywords in critical_keywords.items():
            keyword_matches = sum(1 for kw in keywords if kw in combined_text)
            if keyword_matches >= 2:
                return {
                    "alert_type": alert_type,
                    "severity": "critical" if keyword_matches >= 3 else "high",
                    "confidence": min(0.95, 0.6 + (keyword_matches * 0.15)),
                    "message": f"Potential {alert_type.replace('_', ' ')} detected based on clinical indicators",
                    "recommended_actions": "Notify charge nurse and physician immediately. Assess patient promptly."
                }

        return None


# Singleton instance
ai_service = AIService()
