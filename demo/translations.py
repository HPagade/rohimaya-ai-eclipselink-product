"""Multi-language Translation Support for EclipseLink AI Demo"""

# Translation dictionaries
# In production, this would use Google Translate API or similar
TRANSLATIONS = {
    'en': {
        'dashboard': 'Dashboard',
        'new_handoff': 'New Handoff',
        'patients': 'Patients',
        'analytics': 'Analytics',
        'audit_trail': 'Audit Trail',
        'welcome': 'Welcome back',
        'active_handoffs': 'Active Handoffs',
        'completed_today': 'Completed Today',
        'total_handoffs': 'Total Handoffs',
        'avg_time': 'Avg Time (min)',
        'search': 'Search',
        'filter': 'Filter',
        'all_handoffs': 'All Handoffs',
        'create_handoff': 'Create New Handoff',
        'patient_name': 'Patient Name',
        'patient_id': 'Patient ID',
        'handoff_type': 'Handoff Type',
        'priority': 'Priority',
        'status': 'Status',
        'view': 'View',
        'logout': 'Logout',
        'ai_assistant': 'AI Assistant',
        'family_portal': 'Family Portal',
        'patient_portal': 'Patient Portal',
        'situation': 'Situation',
        'background': 'Background',
        'assessment': 'Assessment',
        'recommendation': 'Recommendation',
    },
    'es': {  # Spanish
        'dashboard': 'Tablero',
        'new_handoff': 'Nuevo Traspaso',
        'patients': 'Pacientes',
        'analytics': 'Analíticas',
        'audit_trail': 'Registro de Auditoría',
        'welcome': 'Bienvenido de nuevo',
        'active_handoffs': 'Traspasos Activos',
        'completed_today': 'Completados Hoy',
        'total_handoffs': 'Total de Traspasos',
        'avg_time': 'Tiempo Promedio (min)',
        'search': 'Buscar',
        'filter': 'Filtrar',
        'all_handoffs': 'Todos los Traspasos',
        'create_handoff': 'Crear Nuevo Traspaso',
        'patient_name': 'Nombre del Paciente',
        'patient_id': 'ID del Paciente',
        'handoff_type': 'Tipo de Traspaso',
        'priority': 'Prioridad',
        'status': 'Estado',
        'view': 'Ver',
        'logout': 'Cerrar Sesión',
        'ai_assistant': 'Asistente de IA',
        'family_portal': 'Portal Familiar',
        'patient_portal': 'Portal del Paciente',
        'situation': 'Situación',
        'background': 'Antecedentes',
        'assessment': 'Evaluación',
        'recommendation': 'Recomendación',
    },
    'zh': {  # Chinese (Simplified)
        'dashboard': '仪表板',
        'new_handoff': '新交接',
        'patients': '患者',
        'analytics': '分析',
        'audit_trail': '审计跟踪',
        'welcome': '欢迎回来',
        'active_handoffs': '活跃交接',
        'completed_today': '今天完成',
        'total_handoffs': '总交接',
        'avg_time': '平均时间（分钟）',
        'search': '搜索',
        'filter': '过滤',
        'all_handoffs': '所有交接',
        'create_handoff': '创建新交接',
        'patient_name': '患者姓名',
        'patient_id': '患者ID',
        'handoff_type': '交接类型',
        'priority': '优先级',
        'status': '状态',
        'view': '查看',
        'logout': '登出',
        'ai_assistant': 'AI助手',
        'family_portal': '家庭门户',
        'patient_portal': '患者门户',
        'situation': '情况',
        'background': '背景',
        'assessment': '评估',
        'recommendation': '建议',
    },
    'fr': {  # French
        'dashboard': 'Tableau de Bord',
        'new_handoff': 'Nouveau Transfert',
        'patients': 'Patients',
        'analytics': 'Analytiques',
        'audit_trail': 'Piste d\'Audit',
        'welcome': 'Bienvenue',
        'active_handoffs': 'Transferts Actifs',
        'completed_today': 'Complétés Aujourd\'hui',
        'total_handoffs': 'Total des Transferts',
        'avg_time': 'Temps Moyen (min)',
        'search': 'Rechercher',
        'filter': 'Filtrer',
        'all_handoffs': 'Tous les Transferts',
        'create_handoff': 'Créer un Nouveau Transfert',
        'patient_name': 'Nom du Patient',
        'patient_id': 'ID du Patient',
        'handoff_type': 'Type de Transfert',
        'priority': 'Priorité',
        'status': 'Statut',
        'view': 'Voir',
        'logout': 'Déconnexion',
        'ai_assistant': 'Assistant IA',
        'family_portal': 'Portail Familial',
        'patient_portal': 'Portail Patient',
        'situation': 'Situation',
        'background': 'Contexte',
        'assessment': 'Évaluation',
        'recommendation': 'Recommandation',
    },
    'ar': {  # Arabic
        'dashboard': 'لوحة القيادة',
        'new_handoff': 'تسليم جديد',
        'patients': 'المرضى',
        'analytics': 'التحليلات',
        'audit_trail': 'سجل التدقيق',
        'welcome': 'مرحباً بعودتك',
        'active_handoffs': 'التسليمات النشطة',
        'completed_today': 'مكتمل اليوم',
        'total_handoffs': 'إجمالي التسليمات',
        'avg_time': 'متوسط ​​الوقت (دقيقة)',
        'search': 'بحث',
        'filter': 'تصفية',
        'all_handoffs': 'جميع التسليمات',
        'create_handoff': 'إنشاء تسليم جديد',
        'patient_name': 'اسم المريض',
        'patient_id': 'معرف المريض',
        'handoff_type': 'نوع التسليم',
        'priority': 'الأولوية',
        'status': 'الحالة',
        'view': 'عرض',
        'logout': 'تسجيل الخروج',
        'ai_assistant': 'مساعد الذكاء الاصطناعي',
        'family_portal': 'بوابة العائلة',
        'patient_portal': 'بوابة المريض',
        'situation': 'الوضع',
        'background': 'الخلفية',
        'assessment': 'التقييم',
        'recommendation': 'التوصية',
    }
}

LANGUAGES = {
    'en': '🇺🇸 English',
    'es': '🇪🇸 Español',
    'zh': '🇨🇳 中文',
    'fr': '🇫🇷 Français',
    'ar': '🇸🇦 العربية'
}


def get_text(key, lang='en'):
    """Get translated text for a key"""
    if lang in TRANSLATIONS and key in TRANSLATIONS[lang]:
        return TRANSLATIONS[lang][key]
    # Fallback to English
    return TRANSLATIONS['en'].get(key, key)


def translate_sbar(sbar_text, target_lang='en'):
    """
    Translate SBAR content to target language
    In production, this would use Google Translate API
    For demo, we use pre-translated medical phrases
    """
    if target_lang == 'en' or not sbar_text:
        return sbar_text

    # Simple translation mappings for common medical terms
    medical_translations = {
        'es': {
            'patient': 'paciente',
            'diabetes': 'diabetes',
            'blood pressure': 'presión arterial',
            'heart rate': 'frecuencia cardíaca',
            'medication': 'medicación',
            'alert and oriented': 'alerta y orientado',
            'vital signs': 'signos vitales',
            'discharge': 'alta',
            'admission': 'ingreso',
        },
        'zh': {
            'patient': '患者',
            'diabetes': '糖尿病',
            'blood pressure': '血压',
            'heart rate': '心率',
            'medication': '药物',
            'alert and oriented': '警觉和定向',
            'vital signs': '生命体征',
            'discharge': '出院',
            'admission': '入院',
        },
        'fr': {
            'patient': 'patient',
            'diabetes': 'diabète',
            'blood pressure': 'tension artérielle',
            'heart rate': 'fréquence cardiaque',
            'medication': 'médicament',
            'alert and oriented': 'alerte et orienté',
            'vital signs': 'signes vitaux',
            'discharge': 'sortie',
            'admission': 'admission',
        }
    }

    translated = sbar_text
    if target_lang in medical_translations:
        for eng, trans in medical_translations[target_lang].items():
            translated = translated.replace(eng, trans)

    return f"[{LANGUAGES[target_lang]}] {translated}"
