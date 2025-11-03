"""
AI Service (SOLID Principles)
Single Responsibility: AI processing for transcription and SBAR generation
Dependency Inversion: Depends on abstract AI providers
Open/Closed: Easy to add new AI providers without modifying existing code
"""
from typing import Protocol, Optional
from abc import abstractmethod
import openai
from anthropic import Anthropic
from app.config import settings
from app.models import (
    TranscriptionResponse,
    SBARGenerationResponse,
    SBARSituation,
    SBARBackground,
    SBARAssessment,
    SBARRecommendation
)
import json


# ============================================================================
# INTERFACES (Dependency Inversion Principle)
# ============================================================================

class TranscriptionProvider(Protocol):
    """Interface for transcription services"""

    @abstractmethod
    async def transcribe(self, audio_url: str, language: str = "en") -> TranscriptionResponse:
        """Transcribe audio to text"""
        ...


class SBARProvider(Protocol):
    """Interface for SBAR generation services"""

    @abstractmethod
    async def generate_sbar(
        self,
        transcription: str,
        patient_context: Optional[dict] = None
    ) -> SBARGenerationResponse:
        """Generate SBAR from transcription"""
        ...


# ============================================================================
# IMPLEMENTATIONS (Open/Closed Principle - easy to add providers)
# ============================================================================

class WhisperTranscriptionProvider:
    """OpenAI Whisper implementation"""

    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)

    async def transcribe(self, audio_url: str, language: str = "en") -> TranscriptionResponse:
        """
        Transcribe audio using OpenAI Whisper
        Single Responsibility: Audio transcription only
        """
        try:
            # Download audio file
            import httpx
            async with httpx.AsyncClient() as client:
                response = await client.get(audio_url)
                audio_content = response.content

            # Save temporarily
            import tempfile
            import os
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                temp_file.write(audio_content)
                temp_path = temp_file.name

            try:
                # Transcribe using Whisper
                with open(temp_path, "rb") as audio_file:
                    transcript = self.client.audio.transcriptions.create(
                        model=settings.OPENAI_WHISPER_MODEL,
                        file=audio_file,
                        language=language,
                        response_format="verbose_json"
                    )

                return TranscriptionResponse(
                    text=transcript.text,
                    confidence=0.95,  # Whisper doesn't provide confidence, use high default
                    duration_seconds=int(transcript.duration) if hasattr(transcript, 'duration') else None
                )
            finally:
                # Clean up temp file
                os.unlink(temp_path)

        except Exception as e:
            raise Exception(f"Transcription failed: {str(e)}")


class ClaudeSBARProvider:
    """Anthropic Claude implementation for SBAR generation"""

    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)
        self.model = settings.ANTHROPIC_MODEL

    async def generate_sbar(
        self,
        transcription: str,
        patient_context: Optional[dict] = None
    ) -> SBARGenerationResponse:
        """
        Generate SBAR using Claude
        Single Responsibility: SBAR generation only
        """
        try:
            # Build context-aware prompt
            context_str = ""
            if patient_context:
                context_str = f"\n\nPatient Context:\n{json.dumps(patient_context, indent=2)}"

            system_prompt = """You are a clinical AI assistant specialized in converting nursing handoff notes into structured SBAR format.

SBAR Format:
- **Situation**: Patient name, age, room, diagnosis, chief complaint
- **Background**: Medical history, surgical history, allergies, current medications, code status
- **Assessment**: Vital signs, lab values, current condition, progress notes, concerns
- **Recommendation**: Pending orders, follow-up needed, escalation requirements, next steps

Extract information from the transcription and structure it according to SBAR format.
Be precise with medical terminology. If information is missing, use null values.
Return ONLY valid JSON matching this exact structure:

{
  "situation": {
    "patient_name": string | null,
    "age": number | null,
    "room": string | null,
    "diagnosis": string | null,
    "chief_complaint": string | null
  },
  "background": {
    "medical_history": [string],
    "surgical_history": [string],
    "allergies": [string],
    "medications": [{"name": string, "dose": string, "route": string, "frequency": string}],
    "code_status": string | null
  },
  "assessment": {
    "vital_signs": {"hr": number, "bp": string, "rr": number, "temp": number, "spo2": number},
    "labs": {},
    "current_condition": string | null,
    "progress": string | null,
    "concerns": [string]
  },
  "recommendation": {
    "pending_orders": [string],
    "follow_up_needed": [string],
    "escalation_required": boolean,
    "next_steps": string | null
  }
}"""

            user_prompt = f"""Transcription of clinical handoff:

{transcription}{context_str}

Generate structured SBAR in JSON format:"""

            # Call Claude API
            message = self.client.messages.create(
                model=self.model,
                max_tokens=settings.ANTHROPIC_MAX_TOKENS,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )

            # Parse response
            response_text = message.content[0].text

            # Extract JSON (Claude might add explanatory text)
            import re
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            if json_match:
                sbar_data = json.loads(json_match.group())
            else:
                sbar_data = json.loads(response_text)

            # Convert to Pydantic models
            return SBARGenerationResponse(
                situation=SBARSituation(**sbar_data.get("situation", {})),
                background=SBARBackground(**sbar_data.get("background", {})),
                assessment=SBARAssessment(**sbar_data.get("assessment", {})),
                recommendation=SBARRecommendation(**sbar_data.get("recommendation", {})),
                quality_score=0.9  # Could implement quality assessment logic here
            )

        except Exception as e:
            raise Exception(f"SBAR generation failed: {str(e)}")


# ============================================================================
# SERVICE CLASS (Dependency Inversion - depends on interfaces, not implementations)
# ============================================================================

class AIService:
    """
    Single Responsibility: Coordinate AI processing
    Dependency Inversion: Depends on abstract providers
    """

    def __init__(
        self,
        transcription_provider: Optional[TranscriptionProvider] = None,
        sbar_provider: Optional[SBARProvider] = None
    ):
        # Use provided providers or create defaults
        self.transcription_provider = transcription_provider or WhisperTranscriptionProvider(
            api_key=settings.OPENAI_API_KEY
        )
        self.sbar_provider = sbar_provider or ClaudeSBARProvider(
            api_key=settings.ANTHROPIC_API_KEY
        )

    async def transcribe_audio(
        self,
        audio_url: str,
        language: str = "en"
    ) -> TranscriptionResponse:
        """
        Transcribe audio file
        Single Responsibility: Delegation to transcription provider
        """
        return await self.transcription_provider.transcribe(audio_url, language)

    async def generate_sbar(
        self,
        transcription: str,
        patient_context: Optional[dict] = None
    ) -> SBARGenerationResponse:
        """
        Generate SBAR from transcription
        Single Responsibility: Delegation to SBAR provider
        """
        return await self.sbar_provider.generate_sbar(transcription, patient_context)

    async def process_handoff_audio(
        self,
        audio_url: str,
        patient_context: Optional[dict] = None,
        language: str = "en"
    ) -> tuple[TranscriptionResponse, SBARGenerationResponse]:
        """
        Complete pipeline: audio -> transcription -> SBAR
        Single Responsibility: Orchestrate full workflow
        """
        # Step 1: Transcribe
        transcription_result = await self.transcribe_audio(audio_url, language)

        # Step 2: Generate SBAR
        sbar_result = await self.generate_sbar(
            transcription_result.text,
            patient_context
        )

        return transcription_result, sbar_result


# ============================================================================
# FACTORY (Dependency Injection)
# ============================================================================

def get_ai_service() -> AIService:
    """
    Factory function for dependency injection
    Makes it easy to mock for testing
    """
    return AIService()
