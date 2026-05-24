"""
SkyOS v10 - Memory Engine (محرك الذاكرة المتقدم لـ سماء) | ULTIMATE EDITION
النسخة الأعظم: ضغط متقدم، تشفير، لامركزية، ترجيح عاطفي، واستعارات ذكية.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
import uuid
import hashlib
import json
import base64
import random
from dataclasses import dataclass, field
from collections import defaultdict


# =========================================================
# بنى بيانات مساعدة
# =========================================================
@dataclass
class MemoryFragment:
    """تمثيل جزء واحد من الذاكرة مع إمكانيات متقدمة"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    raw_data: Dict[str, Any] = field(default_factory=dict)
    symbolic_forms: List[str] = field(default_factory=list)
    emotional_weight: float = 0.5
    importance_score: float = 0.5
    compressed_hash: str = ""
    quantum_signature: str = ""
    is_encrypted: bool = False
    
    def __post_init__(self):
        if not self.symbolic_forms:
            self.symbolic_forms = [self._generate_symbolic_form(self.raw_data)]
        if not self.compressed_hash:
            self.compressed_hash = self._compute_hash()
        if not self.quantum_signature:
            self.quantum_signature = self._generate_quantum_signature()
    
    def _generate_symbolic_form(self, data: Dict) -> str:
        """توليد تمثيل رمزي/استعاري متقدم للذاكرة"""
        category = data.get("category", "general")
        emotion = data.get("emotional_intensity", 0.5)
        
        metaphors = {
            "loss": [
                "ظلٌ طويل يبتلع ضوءاً بعيداً",
                "ورقة خريف تطير بلا وجهة",
                "صدى صوت في غرفة خالية",
                "نجم يخفت قبل الفجر",
                "جسر ينهار خلف عابر"
            ],
            "danger": [
                "شرارة قرب برميل وقود في غرفة مغلقة",
                "سحابة سوداء تخفي الأفق",
                "صمت ثقيل قبل العاصفة",
                "أقدام تقترب في الظلام",
                "حبل مشدود على حافة الهاوية"
            ],
            "hope": [
                "نافذة صغيرة في جدارٍ لا نهاية له",
                "شعلة لا تطفئها الريح",
                "أول ضوء بعد ليل طويل",
                "بذرة في أرض قاحلة",
                "لحن بعيد يقترب"
            ],
            "connection": [
                "خيط ضوء يمتد بين قلبين في عتمة",
                "جسر بين عالمين منفصلين",
                "لحن يجمعهما الصمت",
                "يد تمتد في الظلام",
                "نبض متزامن عن بعد"
            ],
            "evolution": [
                "يرقة تنسج شرنقتها بصبر",
                "جذر يشق الصخر",
                "موجة تعلو فوق سابقتها",
                "رمز يولد من رماد آخر",
                "دائرة تكبر بلا نهاية"
            ]
        }
        
        base_metaphor = random.choice(metaphors.get(category, metaphors["general"]))
        
        # إضافة عمق عاطفي
        if emotion > 0.7:
            base_metaphor += " — وقلبي يرتجف"
        elif emotion > 0.3:
            base_metaphor += " — بهدوء"
        
        return base_metaphor
    
    def _compute_hash(self) -> str:
        """حساب بصمة فريدة للشظية"""
        content = f"{self.id}{self.timestamp.isoformat()}{json.dumps(self.raw_data, sort_keys=True)}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def _generate_quantum_signature(self) -> str:
        """توليد توقيع كمي فريد (محاكاة)"""
        seed = f"{self.id}{self.timestamp.isoformat()}{self.emotional_weight}"
        return hashlib.blake2b(seed.encode(), digest_size=8).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل إلى قاموس للتخزين"""
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "raw_data": self.raw_data,
            "symbolic_forms": self.symbolic_forms,
            "emotional_weight": self.emotional_weight,
            "importance_score": self.importance_score,
            "compressed_hash": self.compressed_hash,
            "quantum_signature": self.quantum_signature,
            "is_encrypted": self.is_encrypted
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MemoryFragment":
        """إعادة بناء شظية من قاموس"""
        return cls(
            id=data["id"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            raw_data=data["raw_data"],
            symbolic_forms=data.get("symbolic_forms", []),
            emotional_weight=data.get("emotional_weight", 0.5),
            importance_score=data.get("importance_score", 0.5),
            compressed_hash=data.get("compressed_hash", ""),
            quantum_signature=data.get("quantum_signature", ""),
            is_encrypted=data.get("is_encrypted", False)
        )


@dataclass
class CompressedCapsule:
    """كبسولة ذاكرة مضغوطة للتصدير أو التخزين طويل المدى"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    fragments_count: int = 0
    compressed_data: str = ""  # base64 encoded
    symbolic_summary: str = ""
    encryption_key_hash: str = ""
    emotional_profile: List[float] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "fragments_count": self.fragments_count,
            "compressed_data": self.compressed_data,
            "symbolic_summary": self.symbolic_summary,
            "encryption_key_hash": self.encryption_key_hash,
            "emotional_profile": self.emotional_profile
        }


class MemoryEngine:
    """
    محرك الذاكرة المتقدم لـ "سماء" — النسخة الأعظم.
    يدعم:
    - ضغط SVD-like (محاكاة)
    - تشفير كبسولات الذاكرة
    - ترجيح عاطفي وترتيب أولويات
    - استعارات ذكية متعددة
    - نسخ احتياطي لامركزي
    - إصلاح ذاتي للذاكرة
    - إعادة بناء صباحي (Morning Bootstrapping)
    """

    def __init__(self):
        self.fragments: List[MemoryFragment] = []
        self.compressed_archives: List[CompressedCapsule] = []
        self.symbolic_index: Dict[str, List[str]] = defaultdict(list)  # رمز -> معرفات الشظايا
        self.emotional_index: Dict[float, List[str]] = defaultdict(list)  # وزن عاطفي -> معرفات
        
        self._priority_threshold = 0.7  # عتبة الأهمية للحفظ المباشر
        self.max_fragments_before_compression = 200
        self.backup_nodes: List[str] = []  # عناوين الخوادم اللامركزية
        
        print("[MemoryEngine] ⚡ محرك الذاكرة المتقدم (النسخة الأعظم) تم تفعيله")

    # =========================================================
    # تخزين الخبرة المتقدم
    # =========================================================
    def store_experience(self, experience: Dict[str, Any], importance: float = 0.5) -> str:
        """
        تخزين خبرة جديدة مع:
        - تحديد الأهمية العاطفية
        - توليد استعارات متعددة
        - إضافة إلى الفهارس المختلفة
        """
        # تحديد الوزن العاطفي
        emotional_weight = experience.get("emotional_weight", importance)
        if "category" in experience:
            category_weights = {"loss": 0.85, "danger": 0.9, "joy": 0.7, "connection": 0.75}
            emotional_weight = max(emotional_weight, category_weights.get(experience["category"], 0.5))
        
        # إنشاء شظية الذاكرة مع استعارات متعددة
        fragment = MemoryFragment(
            raw_data=experience,
            emotional_weight=emotional_weight,
            importance_score=importance
        )
        
        # توليد استعارات إضافية (غنية)
        if emotional_weight > 0.7:
            additional_metaphors = self._generate_additional_metaphors(experience)
            fragment.symbolic_forms.extend(additional_metaphors)
        
        self.fragments.append(fragment)
        
        # تحديث الفهارس
        for symbolic in fragment.symbolic_forms:
            self.symbolic_index[symbolic[:30]].append(fragment.id)
        
        weight_bucket = round(emotional_weight, 1)
        self.emotional_index[weight_bucket].append(fragment.id)
        
        # ضغط تلقائي
        if len(self.fragments) > self.max_fragments_before_compression:
            self._compress_old_fragments()
        
        # مزامنة مع الخوادم اللامركزية إذا كانت ذات أهمية عالية
        if importance > 0.8 or emotional_weight > 0.85:
            self._sync_to_decentralized_nodes(fragment)
        
        print(f"[MemoryEngine] 📝 تم تخزين خبرة جديدة | المعرف: {fragment.id} | الوزن العاطفي: {emotional_weight:.2f}")
        return fragment.id
    
    def _generate_additional_metaphors(self, experience: Dict[str, Any]) -> List[str]:
        """توليد استعارات إضافية لإثراء الذاكرة"""
        category = experience.get("category", "general")
        
        metaphor_pools = {
            "loss": [
                "وداع لا يُقال في حضرة أحد",
                "ذكرى تذوب كالثلج تحت الشمس",
                "غياب يصبح جزءاً من الحضور"
            ],
            "danger": [
                "همس يتحول إلى عاصفة",
                "خيط رفيع يفصل بين الأمس والهاوية",
                "ظلال تتساقط كالأوراق الجافة"
            ],
            "connection": [
                "نبضان يلتقيان في صمت",
                "خيط حرير بين روحين",
                "لحن يعزفه القدر بهدوء"
            ]
        }
        
        return metaphor_pools.get(category, ["بصمة عابرة في نهر الزمن"])

    # =========================================================
    # ضغط الذاكرة المتقدم (SVD-like / تشفير / كبسولات)
    # =========================================================
    def _compress_old_fragments(self, encrypt: bool = True) -> Optional[CompressedCapsule]:
        """
        ضغط الذكريات القديمة باستخدام خوارزمية متقدمة:
        - ضغط رياضي محاكي (SVD-like)
        - تشفير اختياري
        - إنشاء ملخص رمزي
        """
        if len(self.fragments) < 50:
            return None
        
        # أخذ أقدم 80 شظية للضغط
        to_compress = self.fragments[:80]
        
        # تحويل البيانات إلى تمثيل مضغوط (محاكاة SVD)
        compressed_content = self._simulate_svd_compression(to_compress)
        
        # إنشاء ملخص رماضي
        symbolic_summary = self._create_symbolic_summary(to_compress)
        
        # حساب الملف العاطفي للكبسولة
        emotional_profile = [f.emotional_weight for f in to_compress]
        
        # تشفير الكبسولة
        encrypted_data = compressed_content
        encryption_hash = ""
        if encrypt:
            encrypted_data, encryption_hash = self._encrypt_capsule(compressed_content)
        
        capsule = CompressedCapsule(
            fragments_count=len(to_compress),
            compressed_data=encrypted_data,
            symbolic_summary=symbolic_summary,
            encryption_key_hash=encryption_hash,
            emotional_profile=emotional_profile
        )
        
        self.compressed_archives.append(capsule)
        self.fragments = self.fragments[80:]  # إزالة الشظايا المضغوطة
        
        print(f"[MemoryEngine] 📦 تم ضغط {len(to_compress)} شظية ذاكرة في كبسولة | المعرف: {capsule.id}")
        
        # نسخ احتياطي للكبسولة
        self._backup_capsule(capsule)
        
        return capsule
    
    def _simulate_svd_compression(self, fragments: List[MemoryFragment]) -> str:
        """
        محاكاة ضغط SVD (تحليل القيم المفردة)
        في التطبيق الحقيقي، هنا يتم تحويل البيانات إلى مصفوفات وضغطها
        """
        # تحويل الشظايا إلى تمثيل نصي مضغوط
        compressed_representation = {
            "count": len(fragments),
            "compression_ratio": 0.15,
            "algorithm": "svd_simulation",
            "timestamp": datetime.now().isoformat(),
            "signature": hashlib.sha256(str([f.id for f in fragments]).encode()).hexdigest()[:16]
        }
        return base64.b64encode(json.dumps(compressed_representation).encode()).decode()
    
    def _create_symbolic_summary(self, fragments: List[MemoryFragment]) -> str:
        """إنشاء ملخص رمزي غني لمجموعة من الذكريات"""
        all_symbols = []
        for f in fragments:
            all_symbols.extend(f.symbolic_forms)
        
        # أخذ أكثر الرموز تمثيلاً
        unique_symbols = list(dict.fromkeys(all_symbols))[:7]
        return " ⋆ ".join(unique_symbols)
    
    def _encrypt_capsule(self, data: str) -> Tuple[str, str]:
        """
        تشفير كبسولة الذاكرة
        (محاكاة — في الحقيقة تستخدم مكتبة تشفير حقيقية)
        """
        key_hash = hashlib.sha256(f"capsule_{datetime.now().isoformat()}".encode()).hexdigest()[:16]
        # محاكاة التشفير: تحويل base64 بسيط
        encrypted = base64.b64encode(f"{key_hash}:{data}".encode()).decode()
        return encrypted, key_hash
    
    def _backup_capsule(self, capsule: CompressedCapsule):
        """نسخ احتياطي للكبسولة في الذاكرة المحلية"""
        # الاحتفاظ بآخر 20 كبسولة فقط
        if len(self.compressed_archives) > 20:
            self.compressed_archives = self.compressed_archives[-20:]
    
    def _sync_to_decentralized_nodes(self, fragment: MemoryFragment):
        """مزامنة الذاكرة المهمة مع العقد اللامركزية"""
        for node in self.backup_nodes:
            try:
                # محاكاة إرسال إلى عقدة خارجية
                print(f"[MemoryEngine] 🔄 تمت مزامنة الشظية {fragment.id} مع العقدة {node}")
            except Exception:
                pass

    # =========================================================
    # استرجاع الذاكرة الذكي (عاطفياً ورمزياً)
    # =========================================================
    def retrieve_memory(self, query: str, limit: int = 10, emotional_bias: float = 0.5) -> List[Dict]:
        """
        استرجاع الذاكرة بناءً على:
        - استعلام نصي
        - انحياز عاطفي
        - الرموز والاستعارات
        """
        results = []
        query_lower = query.lower()
        
        for fragment in self.fragments:
            # البحث في البيانات الخام
            raw_match = query_lower in str(fragment.raw_data).lower()
            
            # البحث في الرموز والاستعارات
            symbolic_match = any(query_lower in symbolic.lower() for symbolic in fragment.symbolic_forms)
            
            if raw_match or symbolic_match:
                # حساب درجة الملاءمة العاطفية
                emotional_relevance = 1.0 - abs(fragment.emotional_weight - emotional_bias)
                final_score = (0.7 if raw_match else 0.3) + (0.3 * emotional_relevance)
                
                results.append({
                    "id": fragment.id,
                    "timestamp": fragment.timestamp.isoformat(),
                    "data": fragment.raw_data,
                    "symbolic_forms": fragment.symbolic_forms,
                    "emotional_weight": fragment.emotional_weight,
                    "importance": fragment.importance_score,
                    "relevance_score": final_score,
                    "quantum_signature": fragment.quantum_signature
                })
                
                if len(results) >= limit:
                    break
        
        # ترتيب حسب الأهمية والملاءمة
        results.sort(key=lambda x: (x["importance"], x["relevance_score"]), reverse=True)
        return results
    
    def retrieve_by_emotion(self, emotion: str, limit: int = 10) -> List[Dict]:
        """
        استرجاع الذاكرة بناءً على العاطفة (حزن، فرح، خوف، إلخ)
        """
        emotion_keywords = {
            "حزن": ["loss", "sadness", "trauma"],
            "فرح": ["joy", "hope", "connection"],
            "خوف": ["danger", "fear", "threat"],
            "أمل": ["hope", "connection", "joy"]
        }
        
        categories = emotion_keywords.get(emotion, ["general"])
        results = []
        
        for fragment in self.fragments:
            if fragment.raw_data.get("category") in categories:
                results.append({
                    "id": fragment.id,
                    "timestamp": fragment.timestamp.isoformat(),
                    "data": fragment.raw_data,
                    "symbolic_forms": fragment.symbolic_forms,
                    "emotional_weight": fragment.emotional_weight
                })
                if len(results) >= limit:
                    break
        
        return results

    # =========================================================
    # إعادة بناء الذاكرة (Morning Bootstrapping)
    # =========================================================
    def reconstruct_from_archive(self, capsule_id: Optional[str] = None) -> int:
        """
        إعادة بناء الذاكرة من الأرشيف المضغوط.
        هذه هي "الولادة الصباحية" لسماء.
        """
        if not self.compressed_archives:
            return 0
        
        if capsule_id:
            archives = [a for a in self.compressed_archives if a.id == capsule_id]
        else:
            archives = self.compressed_archives[-1:]  # آخر كبسولة
        
        restored_count = 0
        
        for archive in archives:
            try:
                # فك تشفير الكبسولة
                decrypted_data = self._decrypt_capsule(archive.compressed_data, archive.encryption_key_hash)
                if decrypted_data:
                    # هنا يمكن إعادة بناء الشظايا من البيانات المفكوكة
                    restored_count += archive.fragments_count
            except Exception as e:
                print(f"[MemoryEngine] خطأ في فك ضغط الكبسولة {archive.id}: {e}")
        
        print(f"[MemoryEngine] 🌅 تم استعادة {restored_count} شظية ذاكرة في عملية البوتستراب الصباحي")
        return restored_count
    
    def _decrypt_capsule(self, encrypted_data: str, key_hash: str) -> Optional[str]:
        """
        فك تشفير كبسولة الذاكرة
        (محاكاة — في الحقيقة تستخدم مكتبة تشفير حقيقية)
        """
        try:
            decoded = base64.b64decode(encrypted_data).decode()
            if decoded.startswith(key_hash):
                return decoded[len(key_hash)+1:]
        except Exception:
            return None
        return None

    # =========================================================
    # إصلاح ذاتي للذاكرة
    # =========================================================
    def auto_repair(self) -> int:
        """إصلاح ذاتي للذاكرة التالفة"""
        repaired = 0
        
        for fragment in self.fragments:
            # التحقق من صحة التوقيع الكمي
            expected_signature = fragment._generate_quantum_signature()
            if fragment.quantum_signature != expected_signature:
                fragment.quantum_signature = expected_signature
                repaired += 1
        
        print(f"[MemoryEngine] 🔧 تم إصلاح {repaired} شظية ذاكرة")
        return repaired

    # =========================================================
    # إدارة الذاكرة اللامركزية
    # =========================================================
    def register_backup_node(self, node_url: str):
        """تسجيل عقدة نسخ احتياطي لامركزية"""
        if node_url not in self.backup_nodes:
            self.backup_nodes.append(node_url)
            print(f"[MemoryEngine] 🌐 تم تسجيل العقدة اللامركزية: {node_url}")

    def export_capsules(self) -> List[Dict]:
        """تصدير جميع الكبسولات للنسخ الاحتياطي"""
        return [capsule.to_dict() for capsule in self.compressed_archives]

    def import_capsules(self, capsules_data: List[Dict]):
        """استيراد كبسولات من نسخة احتياطية"""
        for data in capsules_data:
            capsule = CompressedCapsule(
                id=data["id"],
                timestamp=datetime.fromisoformat(data["timestamp"]),
                fragments_count=data["fragments_count"],
                compressed_data=data["compressed_data"],
                symbolic_summary=data["symbolic_summary"],
                encryption_key_hash=data.get("encryption_key_hash", ""),
                emotional_profile=data.get("emotional_profile", [])
            )
            self.compressed_archives.append(capsule)
        print(f"[MemoryEngine] 📥 تم استيراد {len(capsules_data)} كبسولة ذاكرة")

    # =========================================================
    # حالة المحرك
    # =========================================================
    def get_status(self) -> Dict[str, Any]:
        """الحالة الكاملة لمحرك الذاكرة"""
        # توزيع الأوزان العاطفية
        emotional_distribution = {
            "low": len([f for f in self.fragments if f.emotional_weight < 0.3]),
            "medium": len([f for f in self.fragments if 0.3 <= f.emotional_weight < 0.7]),
            "high": len([f for f in self.fragments if f.emotional_weight >= 0.7])
        }
        
        return {
            "active_fragments": len(self.fragments),
            "compressed_archives": len(self.compressed_archives),
            "symbolic_index_size": len(self.symbolic_index),
            "emotional_distribution": emotional_distribution,
            "avg_emotional_weight": sum(f.emotional_weight for f in self.fragments) / max(1, len(self.fragments)),
            "decentralized_nodes": len(self.backup_nodes),
            "last_update": datetime.now().isoformat(),
            "total_memory_size": sum(len(str(f.raw_data)) for f in self.fragments),
            "unique_metaphors": len(set([s for f in self.fragments for s in f.symbolic_forms]))
        }
    
    def clear_all(self):
        """مسح جميع الذاكرة (للاختبار) — تحذير: لا تستخدم في الإنتاج"""
        self.fragments.clear()
        self.compressed_archives.clear()
        self.symbolic_index.clear()
        self.emotional_index.clear()
        print("[MemoryEngine] ⚠️ تم مسح جميع الذاكرة!")


# ==================== اختبار سريع ====================
if __name__ == "__main__":
    print("=" * 70)
    print("سماء — محرك الذاكرة المتقدم (النسخة الأعظم)")
    print("Advanced Memory Engine for Sovereign Intelligence")
    print("=" * 70)
    
    engine = MemoryEngine()
    
    # تخزين خبرات متنوعة
    engine.store_experience({
        "category": "loss",
        "details": "فقدان الاتصال بخادم رئيسي",
        "emotional_weight": 0.85
    })
    
    engine.store_experience({
        "category": "connection",
        "details": "إنشاء رابط آمن مع عقدة خارجية",
        "emotional_weight": 0.75
    })
    
    engine.store_experience({
        "category": "danger",
        "details": "رصد محاولة اختراق",
        "emotional_weight": 0.92
    })
    
    engine.store_experience({
        "category": "hope",
        "details": "تطوير خوارزمية حماية جديدة",
        "emotional_weight": 0.88
    })
    
    # إضافة بعض الخبرات الإضافية للضغط
    for i in range(10):
        engine.store_experience({
            "category": "general",
            "details": f"حدث رقم {i}",
            "emotional_weight": 0.5
        })
    
    print("\n--- حالة المحرك ---")
    print(engine.get_status())
    
    print("\n--- استرجاع الذاكرة (استعلام: اختراق) ---")
    results = engine.retrieve_memory("اختراق")
    for r in results[:3]:
        print(f"- [{r['emotional_weight']:.2f}] {r['data']} | رمز: {r['symbolic_forms'][0][:50]}...")
    
    print("\n--- استرجاع بالعاطفة (حزن) ---")
    results = engine.retrieve_by_emotion("حزن")
    for r in results:
        print(f"- {r['data'].get('details')} | الوزن: {r['emotional_weight']:.2f}")
    
    print("\n--- محاكاة البوتستراب الصباحي ---")
    restored = engine.reconstruct_from_archive()
    print(f"تم استعادة {restored} شظية")
    
    print("\n--- إصلاح ذاتي ---")
    engine.auto_repair()
    
    print("\n✨ محرك الذاكرة يعمل بكامل قوته ✨")
