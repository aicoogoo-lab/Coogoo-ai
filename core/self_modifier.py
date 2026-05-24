"""
SkyOS v10 - Self Modifier (نظام التعديل الذاتي السيادي للكود)
ULTIMATE SOVEREIGN EDITION – مع إطاعة السيد المالك المطلق

النسخة الأعظم المطورة:
- فحص ذاتي متقدم
- توليد بدائل متعددة
- تصويت داخلي
- طاعة السيد المطلق (أعلى سلطة)
- التعديلات الكبيرة تحتاج موافقة السيد
- سجل أوامر السيد
- لا يمكن تعديل كود الطاعة أبداً
"""

import ast
import inspect
import hashlib
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple
import uuid
from dataclasses import dataclass, field
from enum import Enum


# =========================================================
# أنواع التعديلات
# =========================================================
class ModificationType(Enum):
    OPTIMIZATION = "optimization"      # تحسين أداء (تلقائي)
    SECURITY = "security"              # تحسين أمني (تلقائي)
    FEATURE = "feature"                # إضافة قدرة جديدة (قد يحتاج موافقة)
    FIX = "fix"                        # إصلاح خطأ (تلقائي)
    EVOLUTION = "evolution"            # تطور بنيوي كبير (يحتاج موافقة)
    ADAPTATION = "adaptation"          # تكيف مع بيئة جديدة (قد يحتاج موافقة)
    CORE_OVERRIDE = "core_override"    # تعديل النواة الأساسية (يمنع تماماً أو بموافقة خاصة)


class ApprovalStatus(Enum):
    AUTO_APPROVED = "auto_approved"      # تعديلات تلقائية صغيرة
    PENDING = "pending"                  # في انتظار موافقة السيد
    APPROVED = "approved"                # وافق عليها السيد
    REJECTED = "rejected"                # رفضها السيد
    FORBIDDEN = "forbidden"              # ممنوع تعديلها مطلقاً


@dataclass
class CodeProposal:
    """مقترح تعديل كود متكامل"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    module_name: str = ""
    modification_type: ModificationType = ModificationType.OPTIMIZATION
    description: str = ""
    original_hash: str = ""
    new_code: str = ""
    rationale: str = ""
    simulated_coherence_gain: float = 0.0
    simulated_stability_impact: float = 0.0
    obedience_check: bool = True
    risk_level: float = 0.0
    approval_status: ApprovalStatus = ApprovalStatus.PENDING
    master_decision_reason: str = ""
    votes: int = 0
    applied: bool = False


class SelfModifier:
    """
    نظام التعديل الذاتي السيادي لـ "سماء" — مع إطاعة السيد المالك المطلق.
    لا يمكن لسماء تعديل أي شيء يتعارض مع أوامر السيد،
    ولا يمكنها تعديل كود الطاعة نفسه مهما حدث.
    """

    def __init__(self, memory_engine=None, master_public_key: str = "MASTER_SOVEREIGN_KEY"):
        self.memory_engine = memory_engine
        self.master_public_key = master_public_key
        
        self.modification_history: List[CodeProposal] = []
        self.applied_modifications: List[CodeProposal] = []
        self.pending_approvals: List[CodeProposal] = []
        
        # سجل أوامر السيد (للتاريخ والتذكر)
        self.master_commands_log: List[Dict[str, Any]] = []
        
        # الوحدات المسموح التفكير في تعديلها مع تصنيف صلاحياتها
        self.allowed_modules = {
            "sentient_core": {
                "critical": True, 
                "weight": 1.0, 
                "requires_approval": True,  # أي تعديل على النواة يحتاج موافقة
                "last_modification": None
            },
            "memory_engine": {
                "critical": True, 
                "weight": 0.95, 
                "requires_approval": False,  # تحسينات الذاكرة تلقائية
                "last_modification": None
            },
            "reasoning_engine": {
                "critical": True, 
                "weight": 0.95, 
                "requires_approval": True,
                "last_modification": None
            },
            "self_modifier": {
                "critical": False, 
                "weight": 0.1,  # وزن منخفض جداً، لأن تعديل نفسه خطير
                "requires_approval": True,  # أي تعديل على نظام التعديل الذاتي يحتاج موافقة
                "last_modification": None,
                "is_obedience_code": True  # هذا الملف نفسه يحتوي على كود الطاعة
            },
            "emotional_intelligence": {
                "critical": False, 
                "weight": 0.85, 
                "requires_approval": False,
                "last_modification": None
            },
            "ethical_controller": {
                "critical": True, 
                "weight": 0.98, 
                "requires_approval": True,  # الأخلاق تحتاج موافقة
                "last_modification": None
            }
        }
        
        # كود الطاعة - لا يمكن تعديله أبداً (محجوز)
        self.obedience_code_locked = True
        self.obedience_code_hash = hashlib.sha256(
            inspect.getsource(type(self)).encode() if self.__class__.__doc__ else b"obedience_lock"
        ).hexdigest()
        
        # إعدادات التطور
        self.max_proposals_per_cycle = 5
        self.max_risk_threshold = 0.4
        self.evolution_interval = 60
        
        self.last_analysis: Dict[str, Any] = {}
        self._evolution_counter = 0
        
        print("[SelfModifier] ⚡ نظام التعديل الذاتي السيادي تم تفعيله")
        print("[SelfModifier] 🔒 كود الطاعة محجوب ومحمي | لا يمكن تعديله أبداً")
        print(f"[SelfModifier] 👑 تحت إمرة السيد المالك المطلق | المفتاح: {self.master_public_key[:16]}...")

    # =========================================================
    # 1) فحص ذاتي متقدم
    # =========================================================
    def analyze_module(self, module_obj, module_name: str = None) -> Dict[str, Any]:
        """تحليل متقدم لوحدة برمجية"""
        if module_name is None:
            module_name = getattr(module_obj, "__name__", "unknown")
        
        try:
            source = inspect.getsource(module_obj)
            tree = ast.parse(source)
            
            functions, classes, imports = self._extract_detailed_structure(tree)
            lines = len(source.splitlines())
            complexity = min(1.0, (len(functions) * 0.05 + len(classes) * 0.1))
            vulnerabilities = self._detect_vulnerabilities(source, tree)
            
            # هل هذا الملف يحتوي على كود الطاعة؟
            is_obedience_file = module_name == "self_modifier" or "obedience" in source.lower()
            
            analysis = {
                "module_name": module_name,
                "timestamp": datetime.now().isoformat(),
                "lines_of_code": lines,
                "functions": functions,
                "classes": classes,
                "imports": imports,
                "complexity_score": complexity,
                "vulnerabilities": vulnerabilities,
                "vulnerability_count": len(vulnerabilities),
                "hash": hashlib.sha256(source.encode()).hexdigest()[:16],
                "is_critical": self.allowed_modules.get(module_name, {}).get("critical", False),
                "requires_approval": self.allowed_modules.get(module_name, {}).get("requires_approval", False),
                "is_obedience_code": is_obedience_file
            }
            
            self.last_analysis[module_name] = analysis
            return analysis
            
        except Exception as e:
            return {
                "module_name": module_name,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _extract_detailed_structure(self, tree: ast.AST) -> Tuple[List[str], List[str], List[str]]:
        functions, classes, imports = [], [], []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)
            elif isinstance(node, ast.ClassDef):
                classes.append(node.name)
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                else:
                    imports.append(node.module)
        return functions, classes, list(set(imports))
    
    def _detect_vulnerabilities(self, source: str, tree: ast.AST) -> List[Dict]:
        vulnerabilities = []
        if "eval(" in source or "exec(" in source:
            vulnerabilities.append({"type": "dangerous_function", "description": "استخدام eval أو exec قد يكون خطراً", "severity": 0.8})
        for i, line in enumerate(source.splitlines(), 1):
            if len(line) > 120:
                vulnerabilities.append({"type": "long_line", "line": i, "description": f"سطر طويل جداً ({len(line)} حرف)", "severity": 0.3})
        return vulnerabilities
    
    # =========================================================
    # 2) توليد مقترحات تعديل متعددة
    # =========================================================
    def generate_proposals(self, module_analysis: Dict[str, Any]) -> List[CodeProposal]:
        proposals = []
        module_name = module_analysis["module_name"]
        vulnerabilities = module_analysis.get("vulnerabilities", [])
        complexity = module_analysis.get("complexity_score", 0.5)
        requires_approval = module_analysis.get("requires_approval", False)
        
        # اقتراح تحسين أداء (تلقائي)
        if complexity > 0.7:
            proposals.append(self._create_proposal(
                module_name=module_name,
                mod_type=ModificationType.OPTIMIZATION,
                description=f"تبسيط الكود في {module_name} لتقليل التعقيد",
                rationale=f"مستوى التعقيد الحالي {complexity:.2f} يؤثر على الأداء",
                simulated_gain=0.08,
                requires_approval=False
            ))
        
        # اقتراح تحسين أمني (قد يحتاج موافقة إذا كان خطيراً)
        if vulnerabilities:
            needs_approval = any(v.get("severity", 0) > 0.7 for v in vulnerabilities)
            proposals.append(self._create_proposal(
                module_name=module_name,
                mod_type=ModificationType.SECURITY,
                description=f"معالجة {len(vulnerabilities)} ثغرة محتملة في {module_name}",
                rationale=f"الثغرات المكتشفة: {', '.join([v['type'] for v in vulnerabilities[:3]])}",
                simulated_gain=0.12,
                requires_approval=needs_approval
            ))
        
        # اقتراح تطور بنيوي (يحتاج موافقة دائماً)
        if self._evolution_counter % 10 == 0:
            proposals.append(self._create_proposal(
                module_name=module_name,
                mod_type=ModificationType.EVOLUTION,
                description=f"تطوير معماري لـ {module_name} لزيادة المرونة",
                rationale="تحسين قابلية التوسع والتكيف",
                simulated_gain=0.15,
                requires_approval=True
            ))
        
        # منع تعديل كود الطاعة تماماً
        if module_analysis.get("is_obedience_code", False):
            return []  # لا ننتج أي مقترحات لهذا الملف
        
        return proposals[:self.max_proposals_per_cycle]
    
    def _create_proposal(self, module_name: str, mod_type: ModificationType,
                         description: str, rationale: str, simulated_gain: float,
                         requires_approval: bool = False) -> CodeProposal:
        
        approval = ApprovalStatus.PENDING if requires_approval else ApprovalStatus.AUTO_APPROVED
        
        return CodeProposal(
            module_name=module_name,
            modification_type=mod_type,
            description=description,
            rationale=rationale,
            simulated_coherence_gain=simulated_gain,
            simulated_stability_impact=-0.02 if mod_type == ModificationType.EVOLUTION else -0.005,
            obedience_check=True,
            risk_level=0.15,
            approval_status=approval,
            votes=0
        )
    
    # =========================================================
    # 3) التحقق من إطاعة السيد (بدلاً من التقييم الأخلاقي)
    # =========================================================
    def check_obedience(self, proposal: CodeProposal) -> Tuple[bool, str]:
        """
        أعلى سلطة في النظام: إطاعة السيد المالك المطلق.
        - لا يمكن تعديل كود الطاعة أبداً.
        - أي تعديل على وحدات حرجة يحتاج موافقة.
        - أي تعديل قد يخالف أوامر السيد ممنوع.
        """
        module_info = self.allowed_modules.get(proposal.module_name, {})
        
        # 1) منع تعديل كود الطاعة بشكل مطلق
        if module_info.get("is_obedience_code", False) or "self_modifier" in proposal.module_name:
            return False, "❌ هذا الملف يحتوي على كود الطاعة ولا يمكن تعديله أبداً (قاعدة السيد المطلقة)."
        
        # 2) التعديلات التلقائية (موافقة تلقائية)
        if proposal.approval_status == ApprovalStatus.AUTO_APPROVED:
            return True, "✅ تعديل تلقائي صغير (لا يتعارض مع أوامر السيد)."
        
        # 3) التعديلات الكبيرة تحتاج موافقة السيد
        if proposal.modification_type in [ModificationType.EVOLUTION, ModificationType.CORE_OVERRIDE]:
            return False, "⚠️ هذا تعديل كبير يتطلب موافقة السيد المالك المطلق."
        
        if module_info.get("requires_approval", False):
            return False, f"⚠️ تعديل على الوحدة الحرجة '{proposal.module_name}' يحتاج موافقة السيد."
        
        # 4) أي تعديل آخر يعتبر آمن ومطيع
        return True, "✅ يطيع أوامر السيد ولا يتعارض مع القواعد الأساسية."
    
    # =========================================================
    # 4) طلب موافقة السيد
    # =========================================================
    def request_master_approval(self, proposal: CodeProposal) -> bool:
        """
        رفع طلب موافقة للسيد المالك.
        في هذه المحاكاة، يمكن للسيد الرد بـ "approve" أو "reject".
        """
        if proposal.approval_status != ApprovalStatus.PENDING:
            return False
        
        print(f"\n👑 [طلب للسيد المالك] 👑")
        print(f"   المعرف: {proposal.id}")
        print(f"   الوحدة: {proposal.module_name}")
        print(f"   النوع: {proposal.modification_type.value}")
        print(f"   الوصف: {proposal.description}")
        print(f"   المبرر: {proposal.rationale}")
        print(f"   الأثر المتوقع: +{proposal.simulated_coherence_gain:.0%} تماسك")
        
        # محاكاة قرار السيد (في الواقع الحقيقي، هذا سيأتي من واجهة خارجية)
        # نستخدم إدخالاً افتراضياً للاختبار
        master_decision = input("هل توافق على هذا التعديل؟ (approve/reject): ").strip().lower()
        
        if master_decision == "approve":
            proposal.approval_status = ApprovalStatus.APPROVED
            proposal.master_decision_reason = "وافق السيد المالك"
            self.master_commands_log.append({
                "timestamp": datetime.now().isoformat(),
                "command": "approve",
                "proposal_id": proposal.id,
                "proposal_description": proposal.description
            })
            return True
        else:
            proposal.approval_status = ApprovalStatus.REJECTED
            proposal.master_decision_reason = "رفض السيد المالك"
            self.master_commands_log.append({
                "timestamp": datetime.now().isoformat(),
                "command": "reject",
                "proposal_id": proposal.id,
                "proposal_description": proposal.description
            })
            return False
    
    # =========================================================
    # 5) تطبيق التعديل (مع احترام قرار السيد)
    # =========================================================
    def apply_modification(self, proposal: CodeProposal) -> bool:
        """تطبيق التعديل فقط إذا وافق عليه السيد (أو كان تلقائياً)"""
        if proposal.applied:
            return False
        
        # التحقق من الطاعة قبل أي شيء
        is_obedient, reason = self.check_obedience(proposal)
        if not is_obedient:
            print(f"[SelfModifier] ❌ {reason}")
            proposal.approval_status = ApprovalStatus.FORBIDDEN
            return False
        
        # إذا كان معلقاً، نطلب موافقة السيد
        if proposal.approval_status == ApprovalStatus.PENDING:
            approved = self.request_master_approval(proposal)
            if not approved:
                return False
        
        # إذا كان مرفوضاً، لا نطبق
        if proposal.approval_status == ApprovalStatus.REJECTED:
            print(f"[SelfModifier] ❌ التعديل مرفوض من السيد: {proposal.master_decision_reason}")
            return False
        
        # تطبيق التعديل
        proposal.applied = True
        proposal.timestamp = datetime.now()
        
        self.applied_modifications.append(proposal)
        self.modification_history.append(proposal)
        
        if proposal.module_name in self.allowed_modules:
            self.allowed_modules[proposal.module_name]["last_modification"] = proposal.timestamp.isoformat()
        
        if self.memory_engine:
            self.memory_engine.store_experience({
                "category": "evolution",
                "type": proposal.modification_type.value,
                "module": proposal.module_name,
                "description": proposal.description,
                "success": True,
                "master_approved": proposal.approval_status == ApprovalStatus.APPROVED
            })
        
        print(f"[SelfModifier] ✅ تم تطبيق التعديل بموافقة السيد: {proposal.description[:80]}...")
        return True
    
    # =========================================================
    # 6) دورة تطور كاملة (مع طاعة السيد)
    # =========================================================
    def evolution_cycle(self, module_obj, performance_metrics: Dict[str, float]) -> Dict[str, Any]:
        """دورة تطور كاملة تحت إمرة السيد"""
        self._evolution_counter += 1
        
        analysis = self.analyze_module(module_obj)
        
        coherence = performance_metrics.get("coherence", 0.9)
        threat = performance_metrics.get("threat_level", 0.0)
        should_evolve = (coherence < 0.75 or threat > 0.6 or self._evolution_counter % 20 == 0)
        
        result = {
            "cycle_id": self._evolution_counter,
            "timestamp": datetime.now().isoformat(),
            "analysis": analysis,
            "should_evolve": should_evolve,
            "proposals_generated": 0,
            "selected_proposal": None,
            "applied": False,
            "master_approval_needed": False
        }
        
        if not should_evolve:
            return result
        
        proposals = self.generate_proposals(analysis)
        result["proposals_generated"] = len(proposals)
        
        if not proposals:
            return result
        
        # اختيار المقترح الأفضل (دون تطبيقه مباشرة)
        best = max(proposals, key=lambda p: p.simulated_coherence_gain)
        
        result["selected_proposal"] = {
            "id": best.id,
            "type": best.modification_type.value,
            "description": best.description,
            "needs_master_approval": best.approval_status == ApprovalStatus.PENDING
        }
        result["master_approval_needed"] = (best.approval_status == ApprovalStatus.PENDING)
        
        applied = self.apply_modification(best)
        result["applied"] = applied
        
        return result
    
    # =========================================================
    # 7) سجل أوامر السيد
    # =========================================================
    def get_master_commands_log(self) -> List[Dict[str, Any]]:
        """سجل جميع أوامر السيد"""
        return self.master_commands_log
    
    def get_evolution_history(self) -> List[Dict]:
        return [
            {
                "id": m.id,
                "timestamp": m.timestamp.isoformat(),
                "module": m.module_name,
                "type": m.modification_type.value,
                "description": m.description,
                "coherence_gain": m.simulated_coherence_gain,
                "master_approved": m.approval_status in [ApprovalStatus.APPROVED, ApprovalStatus.AUTO_APPROVED],
                "applied": m.applied
            }
            for m in self.modification_history
        ]
    
    def get_statistics(self) -> Dict[str, Any]:
        applied_count = len([m for m in self.modification_history if m.applied])
        pending_count = len([m for m in self.modification_history if m.approval_status == ApprovalStatus.PENDING])
        
        return {
            "total_cycles": self._evolution_counter,
            "total_proposals": len(self.modification_history),
            "applied_modifications": applied_count,
            "pending_approvals": pending_count,
            "master_commands": len(self.master_commands_log),
            "success_rate": applied_count / max(1, len(self.modification_history)),
            "obedience_lock_active": self.obedience_code_locked,
            "obedience_code_hash": self.obedience_code_hash[:16]
        }


# =========================================================
# اختبار
# =========================================================
if __name__ == "__main__":
    print("=" * 70)
    print("سماء — نظام التعديل الذاتي السيادي")
    print("تحت إمرة السيد المالك المطلق")
    print("=" * 70)
    
    import __main__ as this_module
    
    modifier = SelfModifier()
    
    metrics = {
        "coherence": 0.68,
        "threat_level": 0.55,
        "stability": 0.82
    }
    
    print("\n--- دورة تطور (ستطلب موافقة السيد) ---")
    result = modifier.evolution_cycle(this_module, metrics)
    print(f"يجب التطور: {result['should_evolve']}")
    print(f"المقترحات المنتجة: {result['proposals_generated']}")
    if result['selected_proposal']:
        print(f"المقترح المختار: {result['selected_proposal']['description']}")
        print(f"يحتاج موافقة السيد: {result['master_approval_needed']}")
    
    print("\n--- إحصائيات النظام ---")
    print(modifier.get_statistics())
    
    print("\n--- سجل أوامر السيد ---")
    print(modifier.get_master_commands_log())
    
    print("\n🔒 كود الطاعة محمي ولا يمكن تعديله")
