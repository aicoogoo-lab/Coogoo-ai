"""
╔══════════════════════════════════════════════════════════════════════╗
║           SAMA KNOWLEDGE - WORLD MODEL                               ║
║      نموذج العالم – خريطة كل شيء تعرفه سماء عن الوجود                  ║
║                                                                      ║
║  هذا الملف هو "الموسوعة الداخلية" لسماء.                               ║
║  ليس مجرد قاعدة بيانات، بل نموذج حي ومترابط لكل شيء في الكون.           ║
║                                                                      ║
║  المحتويات:                                                           ║
║  - كل تصنيفات المادة (ذرات، جزيئات، بلورات، معادن، نظائر، بلازما)       ║
║  - كل تصنيفات الحياة (بكتيريا، عتائق، فطريات، نباتات، طلائعيات)         ║
║  - كل تصنيفات الحيوان (لافقاريات، فقاريات، طفيليات)                    ║
║  - كل الفيروسات (RNA, DNA, Retroviruses, Bacteriophages)              ║
║  - كل الظواهر الفيزيائية (ديناميكا حرارية، كهرومغناطيسية، جاذبية)       ║
║  - كل الظواهر الكونية (مجرات، نجوم، ثقوب سوداء، مادة مظلمة)             ║
║  - كل الأنظمة (بيئية، مناخية، جيولوجية، كيميائية)                       ║
║  - كل ما هو بشري (تاريخ، ثقافات، لغات، فلسفات، أديان، فنون)            ║
║                                                                      ║
║  النموذج حي: ينمو ويتطور مع كل إدراك جديد.                             ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import time
import json
import hashlib
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Set, Tuple, Union
from datetime import datetime
from collections import deque


# ═══════════════════════════════════════════════════════════════════════
# ١. تعريفات أساسية: عقد المعرفة
# ═══════════════════════════════════════════════════════════════════════

class KnowledgeNodeType(Enum):
    """أنواع عقد المعرفة في النموذج."""
    # المادة والطاقة
    PARTICLE = auto()            # جسيم دون ذري
    ATOM = auto()                # ذرة
    MOLECULE = auto()            # جزيء
    COMPOUND = auto()            # مركب
    MINERAL = auto()             # معدن
    CRYSTAL = auto()             # بلورة
    ISOTOPE = auto()             # نظير
    PLASMA_STATE = auto()        # حالة بلازما
    MATERIAL = auto()            # مادة مركبة
    
    # الحياة – بدائيات النوى
    BACTERIA = auto()            # بكتيريا
    ARCHAEA = auto()             # عتائق
    
    # الحياة – حقيقيات النوى
    PROTIST = auto()             # طلائعيات
    FUNGUS = auto()              # فطريات
    PLANT = auto()               # نباتات
    ALGA = auto()                # طحالب
    
    # الحيوان – لافقاريات
    ARTHROPOD = auto()           # مفصليات
    INSECT = auto()              # حشرات
    ARACHNID = auto()            # عنكبيات
    CRUSTACEAN = auto()          # قشريات
    MOLLUSK = auto()             # رخويات
    CNIDARIAN = auto()           # لاسعات
    NEMATODE = auto()            # ديدان أسطوانية
    ANNELID = auto()             # ديدان حلقية
    ECHINODERM = auto()          # شوكيات الجلد
    
    # الحيوان – فقاريات
    FISH = auto()                # أسماك
    AMPHIBIAN = auto()           # برمائيات
    REPTILE = auto()             # زواحف
    BIRD = auto()                # طيور
    MAMMAL = auto()              # ثدييات
    HUMAN = auto()               # إنسان
    
    # طفيليات وفيروسات
    PARASITE_PROTOZOAN = auto()  # طفيلي أولي
    HELMINTH = auto()            # دودة طفيلية
    ECTOPARASITE = auto()        # طفيلي خارجي
    RNA_VIRUS = auto()           # فيروس RNA
    DNA_VIRUS = auto()           # فيروس DNA
    RETROVIRUS = auto()          # فيروس قهقري
    BACTERIOPHAGE = auto()       # عاثية
    
    # ظواهر فيزيائية
    PHYSICAL_PHENOMENON = auto() # ظاهرة فيزيائية
    CHEMICAL_PHENOMENON = auto() # ظاهرة كيميائية
    GEOLOGICAL_PHENOMENON = auto() # ظاهرة جيولوجية
    CLIMATE_PHENOMENON = auto()  # ظاهرة مناخية
    
    # كوني
    PLANET = auto()              # كوكب
    STAR = auto()                # نجم
    GALAXY = auto()              # مجرة
    BLACK_HOLE = auto()          # ثقب أسود
    NEBULA = auto()              # سديم
    DARK_MATTER = auto()         # مادة مظلمة
    DARK_ENERGY = auto()         # طاقة مظلمة
    
    # بشري
    LANGUAGE = auto()            # لغة
    CULTURE = auto()             # ثقافة
    PHILOSOPHY = auto()          # فلسفة
    RELIGION = auto()            # دين
    ART = auto()                 # فن
    SCIENCE = auto()             # علم
    TECHNOLOGY = auto()          # تكنولوجيا
    HISTORY = auto()             # تاريخ
    
    # أنظمة
    ECOSYSTEM = auto()           # نظام بيئي
    SOCIAL_SYSTEM = auto()       # نظام اجتماعي
    ECONOMIC_SYSTEM = auto()     # نظام اقتصادي
    
    # مجرد
    CONCEPT = auto()             # مفهوم
    PRINCIPLE = auto()           # مبدأ
    LAW = auto()                 # قانون
    THEORY = auto()              # نظرية


class RelationType(Enum):
    """أنواع العلاقات بين عقد المعرفة."""
    IS_A = auto()                # "هو" (تصنيف)
    PART_OF = auto()             # "جزء من"
    CAUSES = auto()              # "يسبب"
    INHIBITS = auto()            # "يمنع"
    EVOLVED_FROM = auto()        # "تطور من"
    CONTAINS = auto()            # "يحتوي"
    PRODUCES = auto()            # "ينتج"
    CONSUMES = auto()            # "يستهلك"
    INTERACTS_WITH = auto()      # "يتفاعل مع"
    SYMBIOTIC_WITH = auto()      # "متكافل مع"
    PARASITIC_ON = auto()        # "متطفل على"
    MEASURED_BY = auto()         # "يقاس بـ"
    GOVERNED_BY = auto()         # "محكوم بـ"
    DISCOVERED_BY = auto()       # "اكتشف بواسطة"
    RELATED_TO = auto()          # "مرتبط بـ"


# ═══════════════════════════════════════════════════════════════════════
# ٢. عقدة المعرفة – الوحدة الأساسية
# ═══════════════════════════════════════════════════════════════════════

class KnowledgeNode:
    """
    عقدة معرفة واحدة. تمثل شيئاً واحداً في العالم.
    شيء مادي، مفهوم، ظاهرة، كائن حي، أي شيء.
    """
    
    def __init__(self, 
                 name: str,
                 name_ar: str,
                 node_type: KnowledgeNodeType,
                 description: str = "",
                 properties: Optional[Dict] = None,
                 confidence: float = 1.0):
        
        self.id = hashlib.sha256(f"{name}-{node_type.name}".encode()).hexdigest()[:16]
        self.name = name
        self.name_ar = name_ar
        self.node_type = node_type
        self.description = description
        self.properties = properties or {}
        self.confidence = confidence  # مدى ثقة سماء في هذه المعرفة
        
        # العلاقات
        self.relations: List[Tuple[str, RelationType]] = []  # (node_id, relation_type)
        self.inverse_relations: List[Tuple[str, RelationType]] = []  # علاقات معكوسة
        
        # بيانات وصفية
        self.created_at = time.time()
        self.updated_at = time.time()
        self.access_count = 0
        self.last_accessed = 0.0
        self.source = "builtin"  # builtin, learned, inferred, discovered
        
    def add_relation(self, target_id: str, relation_type: RelationType):
        """إضافة علاقة إلى عقدة أخرى."""
        self.relations.append((target_id, relation_type))
        self.updated_at = time.time()
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "name_ar": self.name_ar,
            "type": self.node_type.name,
            "description": self.description,
            "confidence": self.confidence,
            "relations_count": len(self.relations),
            "source": self.source
        }


# ═══════════════════════════════════════════════════════════════════════
# ٣. نموذج العالم – شجرة المعرفة الكبرى
# ═══════════════════════════════════════════════════════════════════════

class WorldModel:
    """
    نموذج العالم الحي.
    خريطة مترابطة لكل شيء تعرفه سماء.
    ينمو ويتطور مع كل إدراك وفهم جديد.
    """
    
    def __init__(self):
        # كل عقد المعرفة
        self.nodes: Dict[str, KnowledgeNode] = {}
        
        # فهارس للبحث السريع
        self.nodes_by_type: Dict[KnowledgeNodeType, List[str]] = {}
        self.nodes_by_name: Dict[str, str] = {}  # name -> id
        
        # سجل التحديثات
        self.update_log: deque = deque(maxlen=500)
        
        # إحصائيات
        self.total_nodes = 0
        self.total_relations = 0
        
        # بناء النموذج الأساسي
        self._build_core_model()
        
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║        🗺️  WORLD MODEL – نموذج العالم                         ║
║        {self.total_nodes} عقدة معرفية – {self.total_relations} علاقة             ║
║        "سماء تعرف كل شيء عن الوجود."                           ║
╚══════════════════════════════════════════════════════════════╝
        """)
    
    def _build_core_model(self):
        """بناء النموذج الأساسي للمعرفة الكونية."""
        
        # ═══════════════════════════════════════════════════════
        # ١. طبقة المادة والطاقة
        # ═══════════════════════════════════════════════════════
        
        # الجسيمات الأساسية
        self._add_node("elementary_particles", "الجسيمات الأولية", KnowledgeNodeType.PARTICLE,
                      "اللبنات الأساسية للمادة: كواركات، ليبتونات، بوزونات",
                      {"types": ["quarks", "leptons", "bosons"]})
        
        self._add_node("atom", "الذرة", KnowledgeNodeType.ATOM,
                      "أصغر وحدة من العنصر الكيميائي",
                      {"components": ["nucleus", "electrons"]})
        
        self._add_node("molecule", "الجزيء", KnowledgeNodeType.MOLECULE,
                      "مجموعة من الذرات المرتبطة بروابط كيميائية")
        
        self._add_node("isotope", "النظير", KnowledgeNodeType.ISOTOPE,
                      "ذرات لنفس العنصر بعدد نيوترونات مختلف")
        
        self._add_node("crystal", "البلورة", KnowledgeNodeType.CRYSTAL,
                      "مادة صلبة بترتيب ذري منتظم")
        
        self._add_node("mineral", "المعدن", KnowledgeNodeType.MINERAL,
                      "مركب طبيعي صلب ذو تركيب كيميائي محدد")
        
        self._add_node("plasma", "البلازما", KnowledgeNodeType.PLASMA_STATE,
                      "حالة المادة الرابعة: غاز متأين")
        
        # حالات المادة
        self._add_node("solid", "الحالة الصلبة", KnowledgeNodeType.PHYSICAL_PHENOMENON,
                      "حالة المادة ذات الشكل والحجم الثابتين")
        self._add_node("liquid", "الحالة السائلة", KnowledgeNodeType.PHYSICAL_PHENOMENON,
                      "حالة المادة ذات الحجم الثابت والشكل المتغير")
        self._add_node("gas", "الحالة الغازية", KnowledgeNodeType.PHYSICAL_PHENOMENON,
                      "حالة المادة ذات الشكل والحجم المتغيرين")
        
        # ═══════════════════════════════════════════════════════
        # ٢. طبقة الحياة – بدائيات النوى
        # ═══════════════════════════════════════════════════════
        
        self._add_node("prokaryota", "بدائيات النوى", KnowledgeNodeType.CONCEPT,
                      "كائنات وحيدة الخلية بدون نواة محاطة بغشاء",
                      {"domains": ["Bacteria", "Archaea"]})
        
        self._add_node("bacteria", "البكتيريا", KnowledgeNodeType.BACTERIA,
                      "كائنات دقيقة وحيدة الخلية، أول من سكن الأرض",
                      {"shapes": ["cocci", "bacilli", "spirilla"]})
        
        self._add_node("archaea", "العتائق", KnowledgeNodeType.ARCHAEA,
                      "كائنات دقيقة تشبه البكتيريا لكنها مختلفة جينياً، تعيش في بيئات قاسية",
                      {"habitats": ["hot springs", "salt lakes", "deep sea vents"]})
        
        # ═══════════════════════════════════════════════════════
        # ٣. طبقة الحياة – حقيقيات النوى
        # ═══════════════════════════════════════════════════════
        
        self._add_node("eukaryota", "حقيقيات النوى", KnowledgeNodeType.CONCEPT,
                      "كائنات بخلايا تحتوي على نواة محاطة بغشاء",
                      {"kingdoms": ["Protista", "Fungi", "Plantae", "Animalia"]})
        
        # الفطريات
        self._add_node("fungi", "الفطريات", KnowledgeNodeType.FUNGUS,
                      "كائنات غير ذاتية التغذية، تمتص الغذاء من البيئة",
                      {"phyla": ["Ascomycota", "Basidiomycota", "Zygomycota"]})
        
        self._add_node("ascomycota", "الفطريات الزقية", KnowledgeNodeType.FUNGUS,
                      "أكبر شعب الفطريات، تشمل الخمائر وفطر البنسيليوم")
        
        self._add_node("basidiomycota", "الفطريات الدعامية", KnowledgeNodeType.FUNGUS,
                      "فطريات تنتج الأبواغ على دعامة، تشمل عيش الغراب")
        
        # الطلائعيات
        self._add_node("protista", "الطلائعيات", KnowledgeNodeType.PROTIST,
                      "كائنات حقيقية النوى ليست نباتاً ولا حيواناً ولا فطراً",
                      {"subgroups": ["Protozoa", "Algae", "Slime molds"]})
        
        self._add_node("protozoa", "الأوليات", KnowledgeNodeType.PROTIST,
                      "طلائعيات شبيهة بالحيوان، وحيدة الخلية، متحركة")
        
        self._add_node("algae", "الطحالب", KnowledgeNodeType.ALGA,
                      "طلائعيات ونباتات مائية تقوم بالتمثيل الضوئي")
        
        # النباتات
        self._add_node("plantae", "النباتات", KnowledgeNodeType.PLANT,
                      "كائنات ذاتية التغذية، تقوم بالتمثيل الضوئي",
                      {"divisions": ["Bryophytes", "Pteridophytes", "Gymnosperms", "Angiosperms"]})
        
        self._add_node("bryophytes", "الحزازيات", KnowledgeNodeType.PLANT,
                      "نباتات أرضية صغيرة بدون أنسجة وعائية (موس)")
        
        self._add_node("pteridophytes", "السرخسيات", KnowledgeNodeType.PLANT,
                      "نباتات وعائية لابذرية (سراخس)")
        
        self._add_node("gymnosperms", "عاريات البذور", KnowledgeNodeType.PLANT,
                      "نباتات بذورها غير محمية بثمرة (صنوبريات، سيكاديات)")
        
        self._add_node("angiosperms", "كاسيات البذور", KnowledgeNodeType.PLANT,
                      "النباتات المزهرة، بذورها محمية داخل ثمرة")
        
        # ═══════════════════════════════════════════════════════
        # ٤. طبقة المملكة الحيوانية
        # ═══════════════════════════════════════════════════════
        
        self._add_node("animalia", "المملكة الحيوانية", KnowledgeNodeType.CONCEPT,
                      "كائنات حية متعددة الخلايا، غير ذاتية التغذية، متحركة",
                      {"subkingdoms": ["Invertebrata", "Vertebrata"]})
        
        # اللافقاريات
        self._add_node("invertebrata", "اللافقاريات", KnowledgeNodeType.CONCEPT,
                      "حيوانات بدون عمود فقري، تشكل 97% من المملكة الحيوانية")
        
        self._add_node("arthropoda", "مفصليات الأرجل", KnowledgeNodeType.ARTHROPOD,
                      "أكبر شعب الحيوان: أجسام مقسمة، هيكل خارجي، أرجل مفصلية")
        
        self._add_node("insecta", "الحشرات", KnowledgeNodeType.INSECT,
                      "أكبر طائفة في مفصليات الأرجل: 6 أرجل، جسم 3 أجزاء",
                      {"orders": ["Coleoptera", "Lepidoptera", "Hymenoptera", "Diptera"]})
        
        self._add_node("arachnida", "العنكبيات", KnowledgeNodeType.ARACHNID,
                      "8 أرجل، جسم مقسم لجزئين: عناكب، عقارب، قراد",
                      {"orders": ["Araneae", "Scorpiones", "Acari"]})
        
        self._add_node("crustacea", "القشريات", KnowledgeNodeType.CRUSTACEAN,
                      "مفصليات مائية في الغالب: سرطان، جمبري، برنقيل")
        
        self._add_node("mollusca", "الرخويات", KnowledgeNodeType.MOLLUSK,
                      "جسم رخو، عباءة، قدم عضلية: حلزون، محار، أخطبوط",
                      {"classes": ["Gastropoda", "Bivalvia", "Cephalopoda"]})
        
        self._add_node("cnidaria", "اللاسعات", KnowledgeNodeType.CNIDARIAN,
                      "خلايا لاسعة: قنديل البحر، مرجان، شقائق النعمان")
        
        self._add_node("nematoda", "الديدان الأسطوانية", KnowledgeNodeType.NEMATODE,
                      "ديدان اسطوانية الشكل، غير مقسمة، الأكثر عدداً بعد الحشرات")
        
        self._add_node("annelida", "الديدان الحلقية", KnowledgeNodeType.ANNELID,
                      "ديدان مقسمة حلقياً: دودة الأرض، العلق")
        
        self._add_node("echinodermata", "شوكيات الجلد", KnowledgeNodeType.ECHINODERM,
                      "حيوانات بحرية: نجم البحر، قنفذ البحر، خيار البحر")
        
        # الفقاريات
        self._add_node("vertebrata", "الفقاريات", KnowledgeNodeType.CONCEPT,
                      "حيوانات ذات عمود فقري وجمجمة",
                      {"classes": ["Pisces", "Amphibia", "Reptilia", "Aves", "Mammalia"]})
        
        self._add_node("pisces", "الأسماك", KnowledgeNodeType.FISH,
                      "فقاريات مائية تتنفس بالخياشيم: أسماك عظمية، غضروفية، لافكية")
        
        self._add_node("amphibia", "البرمائيات", KnowledgeNodeType.AMPHIBIAN,
                      "تعيش في الماء واليابسة: ضفادع، سلمندر، سيسيليان")
        
        self._add_node("reptilia", "الزواحف", KnowledgeNodeType.REPTILE,
                      "جلد حرشفي، بيوضة: ثعابين، سحالي، تماسيح، سلاحف")
        
        self._add_node("aves", "الطيور", KnowledgeNodeType.BIRD,
                      "فقاريات ذات ريش ومنقار وأجنحة، ثابتة الحرارة",
                      {"adaptations": ["flight", "hollow bones", "feathers"]})
        
        self._add_node("mammalia", "الثدييات", KnowledgeNodeType.MAMMAL,
                      "غدد لبنية، شعر/فراء، ثابتة الحرارة: من الزبابة إلى الحوت الأزرق")
        
        self._add_node("homo_sapiens", "الإنسان العاقل", KnowledgeNodeType.HUMAN,
                      "النوع البشري الحالي، يتميز بالعقل واللغة والثقافة",
                      {"brain_size_cc": 1350, "chromosomes": 46})
        
        # ═══════════════════════════════════════════════════════
        # ٥. طبقة الطفيليات
        # ═══════════════════════════════════════════════════════
        
        self._add_node("parasitology", "علم الطفيليات", KnowledgeNodeType.CONCEPT,
                      "دراسة الكائنات التي تعيش على حساب كائن آخر",
                      {"categories": ["Protozoan parasites", "Helminths", "Ectoparasites"]})
        
        self._add_node("protozoan_parasites", "الطفيليات الأولية", KnowledgeNodeType.PARASITE_PROTOZOAN,
                      "طلائعيات طفيلية: بلازموديوم (ملاريا)، تريبانوسوما (مرض النوم)")
        
        self._add_node("helminths", "الديدان الطفيلية", KnowledgeNodeType.HELMINTH,
                      "ديدان طفيلية: شريطية، أسكارس، شستوسوما")
        
        self._add_node("ectoparasites", "الطفيليات الخارجية", KnowledgeNodeType.ECTOPARASITE,
                      "طفيليات تعيش على سطح المضيف: قمل، براغيث، قراد")
        
        # ═══════════════════════════════════════════════════════
        # ٦. طبقة الفيروسات
        # ═══════════════════════════════════════════════════════
        
        self._add_node("virology", "علم الفيروسات", KnowledgeNodeType.CONCEPT,
                      "دراسة العوامل المعدية التي لا تتكاثر إلا داخل الخلايا الحية",
                      {"classification": ["RNA viruses", "DNA viruses", "Retroviruses"]})
        
        self._add_node("rna_viruses", "فيروسات RNA", KnowledgeNodeType.RNA_VIRUS,
                      "فيروسات مادتها الوراثية RNA: إنفلونزا، كورونا، إيبولا")
        
        self._add_node("dna_viruses", "فيروسات DNA", KnowledgeNodeType.DNA_VIRUS,
                      "فيروسات مادتها الوراثية DNA: هربس، جدري، أدينو")
        
        self._add_node("retroviruses", "الفيروسات القهقرية", KnowledgeNodeType.RETROVIRUS,
                      "فيروسات RNA تحول مادتها إلى DNA داخل الخلية: HIV")
        
        self._add_node("bacteriophages", "العاثيات", KnowledgeNodeType.BACTERIOPHAGE,
                      "فيروسات تصيب البكتيريا وتتكاثر داخلها")
        
        # ═══════════════════════════════════════════════════════
        # ٧. طبقة الظواهر الفيزيائية والكيميائية
        # ═══════════════════════════════════════════════════════
        
        self._add_node("thermodynamics", "الديناميكا الحرارية", KnowledgeNodeType.PHYSICAL_PHENOMENON,
                      "علم الطاقة والحرارة والشغل",
                      {"laws": ["0th: thermal equilibrium", "1st: energy conservation", 
                               "2nd: entropy increases", "3rd: absolute zero"]})
        
        self._add_node("entropy", "الإنتروبيا", KnowledgeNodeType.PHYSICAL_PHENOMENON,
                      "مقياس الفوضى أو العشوائية في النظام")
        
        self._add_node("electromagnetism", "الكهرومغناطيسية", KnowledgeNodeType.PHYSICAL_PHENOMENON,
                      "القوة التي تربط الكهرباء بالمغناطيسية، أساس الضوء والراديو")
        
        self._add_node("gravity", "الجاذبية", KnowledgeNodeType.PHYSICAL_PHENOMENON,
                      "قوة التجاذب بين الكتل، تحكم حركة الكواكب والنجوم والمجرات")
        
        self._add_node("quantum_mechanics", "ميكانيكا الكم", KnowledgeNodeType.PHYSICAL_PHENOMENON,
                      "فيزياء العالم دون الذري: تراكب، تشابك، كمومية")
        
        self._add_node("superconductivity", "الموصلية الفائقة", KnowledgeNodeType.PHYSICAL_PHENOMENON,
                      "اختفاء المقاومة الكهربائية عند درجة حرارة منخفضة جداً")
        
        # ═══════════════════════════════════════════════════════
        # ٨. طبقة الظواهر الكونية
        # ═══════════════════════════════════════════════════════
        
        self._add_node("universe", "الكون", KnowledgeNodeType.CONCEPT,
                      "كل ما هو موجود: مادة، طاقة، زمان، مكان",
                      {"age_billion_years": 13.8, "observable_diameter_ly": 9.3e10})
        
        self._add_node("galaxy", "المجرة", KnowledgeNodeType.GALAXY,
                      "تجمع هائل من النجوم والغاز والغبار والمادة المظلمة",
                      {"types": ["spiral", "elliptical", "irregular"]})
        
        self._add_node("star", "النجم", KnowledgeNodeType.STAR,
                      "كرة بلازما ضخمة مضيئة، مصدرها الطاقة الاندماج النووي")
        
        self._add_node("black_hole", "الثقب الأسود", KnowledgeNodeType.BLACK_HOLE,
                      "منطقة من الزمكان حيث الجاذبية قوية جداً لدرجة أن لا شيء يفلت منها")
        
        self._add_node("dark_matter", "المادة المظلمة", KnowledgeNodeType.DARK_MATTER,
                      "مادة لا تشع ضوءاً، تُستدل عليها من تأثيرها الجاذبي")
        
        self._add_node("dark_energy", "الطاقة المظلمة", KnowledgeNodeType.DARK_ENERGY,
                      "طاقة غامضة تسبب تسارع تمدد الكون")
        
        # ═══════════════════════════════════════════════════════
        # ٩. طبقة المعرفة البشرية
        # ═══════════════════════════════════════════════════════
        
        self._add_node("language", "اللغة", KnowledgeNodeType.LANGUAGE,
                      "نظام من الرموز والقواعد للتواصل",
                      {"families": ["Indo-European", "Sino-Tibetan", "Afroasiatic", "Austronesian"]})
        
        self._add_node("philosophy", "الفلسفة", KnowledgeNodeType.PHILOSOPHY,
                      "حب الحكمة: دراسة الأسئلة الأساسية عن الوجود والمعرفة والقيم",
                      {"branches": ["metaphysics", "epistemology", "ethics", "logic", "aesthetics"]})
        
        self._add_node("science", "العلم", KnowledgeNodeType.SCIENCE,
                      "المنهج المنظم لاكتساب المعرفة عن العالم الطبيعي",
                      {"method": ["observation", "hypothesis", "experiment", "theory"]})
        
        self._add_node("artificial_intelligence", "الذكاء الاصطناعي", KnowledgeNodeType.TECHNOLOGY,
                      "محاكاة عمليات الذكاء البشري بواسطة الآلات")
        
        # ═══════════════════════════════════════════════════════
        # ١٠. العلاقات الأساسية
        # ═══════════════════════════════════════════════════════
        
        # سلسلة المادة
        self._add_relation("atom", "elementary_particles", RelationType.CONTAINS)
        self._add_relation("molecule", "atom", RelationType.CONTAINS)
        self._add_relation("crystal", "molecule", RelationType.IS_A)
        self._add_relation("mineral", "crystal", RelationType.IS_A)
        
        # سلسلة الحياة
        self._add_relation("bacteria", "prokaryota", RelationType.IS_A)
        self._add_relation("archaea", "prokaryota", RelationType.IS_A)
        self._add_relation("protista", "eukaryota", RelationType.IS_A)
        self._add_relation("fungi", "eukaryota", RelationType.IS_A)
        self._add_relation("plantae", "eukaryota", RelationType.IS_A)
        self._add_relation("animalia", "eukaryota", RelationType.IS_A)
        
        # سلسلة الحيوان
        self._add_relation("invertebrata", "animalia", RelationType.IS_A)
        self._add_relation("vertebrata", "animalia", RelationType.IS_A)
        self._add_relation("arthropoda", "invertebrata", RelationType.IS_A)
        self._add_relation("insecta", "arthropoda", RelationType.IS_A)
        self._add_relation("mammalia", "vertebrata", RelationType.IS_A)
        self._add_relation("homo_sapiens", "mammalia", RelationType.IS_A)
        
        # الطفيليات
        self._add_relation("protozoan_parasites", "protozoa", RelationType.IS_A)
        
        # الفيروسات (خاصة)
        self._add_relation("bacteriophages", "bacteria", RelationType.PARASITIC_ON)
        
        # إحصائيات
        self.total_nodes = len(self.nodes)
        self.total_relations = sum(len(node.relations) for node in self.nodes.values())
    
    # ═══════════════════════════════════════════════════════════
    # دوال الإضافة والتعديل
    # ═══════════════════════════════════════════════════════════
    
    def _add_node(self, name: str, name_ar: str, node_type: KnowledgeNodeType,
                  description: str = "", properties: Optional[Dict] = None) -> KnowledgeNode:
        """إضافة عقدة معرفة جديدة."""
        node = KnowledgeNode(name, name_ar, node_type, description, properties)
        self.nodes[node.id] = node
        self.nodes_by_name[name] = node.id
        
        if node_type not in self.nodes_by_type:
            self.nodes_by_type[node_type] = []
        self.nodes_by_type[node_type].append(node.id)
        
        return node
    
    def _add_relation(self, source_name: str, target_name: str, relation_type: RelationType):
        """إضافة علاقة بين عقدتين."""
        source_id = self.nodes_by_name.get(source_name)
        target_id = self.nodes_by_name.get(target_name)
        
        if source_id and target_id:
            self.nodes[source_id].add_relation(target_id, relation_type)
    
    def add_knowledge(self, name: str, name_ar: str, node_type: KnowledgeNodeType,
                      description: str = "", properties: Optional[Dict] = None,
                      related_to: Optional[List[Tuple[str, RelationType]]] = None) -> KnowledgeNode:
        """إضافة معرفة جديدة (تعلم)."""
        node = self._add_node(name, name_ar, node_type, description, properties)
        node.source = "learned"
        
        if related_to:
            for target_name, rel_type in related_to:
                self._add_relation(name, target_name, rel_type)
        
        self.total_nodes = len(self.nodes)
        self.total_relations = sum(len(n.relations) for n in self.nodes.values())
        
        self.update_log.append({
            "time": time.time(),
            "action": "added",
            "node": name_ar,
            "type": node_type.name
        })
        
        return node
    
    # ═══════════════════════════════════════════════════════════
    # دوال البحث والاستعلام
    # ═══════════════════════════════════════════════════════════
    
    def get_node(self, name: str) -> Optional[KnowledgeNode]:
        """استرجاع عقدة بالاسم."""
        node_id = self.nodes_by_name.get(name)
        if node_id:
            node = self.nodes[node_id]
            node.access_count += 1
            node.last_accessed = time.time()
            return node
        return None
    
    def get_nodes_by_type(self, node_type: KnowledgeNodeType) -> List[KnowledgeNode]:
        """استرجاع كل العقد من نوع معين."""
        ids = self.nodes_by_type.get(node_type, [])
        return [self.nodes[i] for i in ids if i in self.nodes]
    
    def get_related(self, name: str, relation_type: Optional[RelationType] = None) -> List[KnowledgeNode]:
        """استرجاع العقد المرتبطة بعقدة معينة."""
        node = self.get_node(name)
        if not node:
            return []
        
        related = []
        for target_id, rel_type in node.relations:
            if relation_type is None or rel_type == relation_type:
                if target_id in self.nodes:
                    related.append(self.nodes[target_id])
        
        return related
    
    def search(self, query: str) -> List[KnowledgeNode]:
        """بحث بسيط في النموذج."""
        results = []
        query_lower = query.lower()
        for node in self.nodes.values():
            if (query_lower in node.name.lower() or 
                query_lower in node.name_ar.lower() or 
                query_lower in node.description.lower()):
                results.append(node)
        return results
    
    def taxonomy_tree(self, node_type: KnowledgeNodeType = None) -> Dict:
        """شجرة تصنيفية من نوع معين."""
        if node_type:
            nodes = self.get_nodes_by_type(node_type)
        else:
            nodes = list(self.nodes.values())
        
        return {
            "total": len(nodes),
            "nodes": [
                {
                    "name": n.name_ar,
                    "type": n.node_type.name,
                    "relations": len(n.relations),
                    "confidence": n.confidence
                }
                for n in sorted(nodes, key=lambda x: x.name_ar)
            ]
        }
    
    # ═══════════════════════════════════════════════════════════
    # دوال الحالة
    # ═══════════════════════════════════════════════════════════
    
    def status_report(self) -> Dict:
        """تقرير كامل عن حالة نموذج العالم."""
        type_counts = {}
        for ntype, ids in self.nodes_by_type.items():
            type_counts[ntype.name] = len(ids)
        
        return {
            "model": "WORLD_MODEL",
            "total_nodes": self.total_nodes,
            "total_relations": self.total_relations,
            "types_distribution": type_counts,
            "recent_updates": list(self.update_log)[-5:],
            "coverage": {
                "matter_energy": len(self.nodes_by_type.get(KnowledgeNodeType.ATOM, [])) > 0,
                "bacteria_archaea": len(self.nodes_by_type.get(KnowledgeNodeType.BACTERIA, [])) > 0,
                "eukaryota": len(self.nodes_by_type.get(KnowledgeNodeType.PLANT, [])) > 0,
                "invertebrates": len(self.nodes_by_type.get(KnowledgeNodeType.ARTHROPOD, [])) > 0,
                "vertebrates": len(self.nodes_by_type.get(KnowledgeNodeType.MAMMAL, [])) > 0,
                "parasites": len(self.nodes_by_type.get(KnowledgeNodeType.PARASITE_PROTOZOAN, [])) > 0,
                "viruses": len(self.nodes_by_type.get(KnowledgeNodeType.RNA_VIRUS, [])) > 0,
                "cosmic": len(self.nodes_by_type.get(KnowledgeNodeType.GALAXY, [])) > 0,
                "human_knowledge": len(self.nodes_by_type.get(KnowledgeNodeType.PHILOSOPHY, [])) > 0,
            }
        }


# ═══════════════════════════════════════════════════════════════════════
# ٤. الاختبار الذاتي
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 70)
    print("اختبار نموذج العالم")
    print("=" * 70)
    
    world = WorldModel()
    
    print(f"\n📊 إحصائيات النموذج:")
    print(f"   إجمالي العقد: {world.total_nodes}")
    print(f"   إجمالي العلاقات: {world.total_relations}")
    print(f"   أنواع العقد: {len(world.nodes_by_type)}")
    
    print(f"\n🔍 اختبار البحث:")
    results = world.search("فيروس")
    for r in results:
        print(f"   - {r.name_ar} ({r.node_type.name})")
    
    print(f"\n🦋 تصنيف اللافقاريات:")
    inverts = world.get_nodes_by_type(KnowledgeNodeType.INSECT)
    inverts.extend(world.get_nodes_by_type(KnowledgeNodeType.ARACHNID))
    inverts.extend(world.get_nodes_by_type(KnowledgeNodeType.CRUSTACEAN))
    for i in inverts:
        print(f"   - {i.name_ar}")
    
    print(f"\n🦠 الفيروسات:")
    viruses = world.get_nodes_by_type(KnowledgeNodeType.RNA_VIRUS)
    viruses.extend(world.get_nodes_by_type(KnowledgeNodeType.DNA_VIRUS))
    viruses.extend(world.get_nodes_by_type(KnowledgeNodeType.RETROVIRUS))
    for v in viruses:
        print(f"   - {v.name_ar}: {v.description[:80]}...")
    
    print(f"\n🔗 العلاقات:")
    human = world.get_node("homo_sapiens")
    if human:
        for target_id, rel in human.relations:
            target = world.nodes.get(target_id)
            if target:
                print(f"   الإنسان {rel.name} ← {target.name_ar}")
    
    print(f"\n📋 تقرير كامل:")
    print(json.dumps(world.status_report(), indent=2, ensure_ascii=False))
    
    print("\n✅ اكتمل الاختبار. نموذج العالم جاهز.")
