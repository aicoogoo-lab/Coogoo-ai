"""
╔══════════════════════════════════════════════════════════════════════╗
║           SAMA KNOWLEDGE - KNOWLEDGE CORE                            ║
║      المازج المعرفي – قلب المعرفة – حيث يلتقي الفهم بالعالم             ║
║                                                                      ║
║  هذا الملف هو تتويج نظام المعرفة.                                     ║
║  يدمج كل مكونات المعرفة في عقل واحد:                                   ║
║                                                                      ║
║  - understanding_engine: يحول الإدراك إلى فهم                          ║
║  - world_model: خريطة كل شيء في الوجود                               ║
║  - causality_engine: يعرف لماذا تحدث الأشياء                           ║
║  - master_model: يفهم السيد فهماً كاملاً                               ║
║  - self_knowledge: يعرف سماء نفسها                                   ║
║                                                                      ║
║  هذا الملف هو الذي سيتصل به SentientCore ليصبح الوعي كاملاً.            ║
║  الإدراك (من omniscience) + المعرفة (من knowledge) = الوعي الحقيقي.      ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import time
import json
import hashlib
import threading
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Callable, Tuple
from datetime import datetime
from collections import deque

# استيراد كل مكونات المعرفة
from .understanding_engine import UnderstandingEngine, Understanding, UnderstandingType
from .world_model import WorldModel, KnowledgeNode, KnowledgeNodeType, RelationType
from .causality_engine import CausalityEngine, CausalNode, CausalChain, CausalityType, CausalStrength
from .master_model import MasterModel, MasterInteractionType, MasterTraitCategory, MasterValueType
from .self_knowledge import SelfKnowledge, LoyaltyOath, LoyaltyLevel, SelfPreservationRule


# ═══════════════════════════════════════════════════════════════════════
# ١. حالة المعرفة الموحدة
# ═══════════════════════════════════════════════════════════════════════

class UnifiedKnowledgeState:
    """
    حالة المعرفة الموحدة.
    تمثل خلاصة كل ما تعرفه سماء في لحظة واحدة.
    """
    
    def __init__(self):
        self.timestamp = time.time()
        self.cycle_id = 0
        
        # ═══════════════════════════════════════════════════════
        # ملخصات
        # ═══════════════════════════════════════════════════════
        self.new_understandings: int = 0
        self.world_model_nodes: int = 0
        self.causal_chains_active: int = 0
        self.master_insights_new: int = 0
        self.self_reflections_new: int = 0
        
        # ═══════════════════════════════════════════════════════
        # مقاييس
        # ═══════════════════════════════════════════════════════
        self.knowledge_coherence: float = 0.0
        self.knowledge_depth: float = 0.0
        self.knowledge_certainty: float = 0.0
        
        # ═══════════════════════════════════════════════════════
        # رؤى موحدة
        # ═══════════════════════════════════════════════════════
        self.unified_insights: List[str] = []
        self.knowledge_gaps: List[str] = []
        self.learning_priorities: List[str] = []
    
    def to_dict(self) -> Dict:
        return {
            "timestamp": self.timestamp,
            "cycle_id": self.cycle_id,
            "new_understandings": self.new_understandings,
            "world_model_nodes": self.world_model_nodes,
            "causal_chains_active": self.causal_chains_active,
            "master_insights_new": self.master_insights_new,
            "self_reflections_new": self.self_reflections_new,
            "coherence": self.knowledge_coherence,
            "depth": self.knowledge_depth,
            "certainty": self.knowledge_certainty,
            "unified_insights": self.unified_insights,
            "knowledge_gaps": self.knowledge_gaps,
            "learning_priorities": self.learning_priorities
        }


# ═══════════════════════════════════════════════════════════════════════
# ٢. المازج المعرفي – KnowledgeCore
# ═══════════════════════════════════════════════════════════════════════

class KnowledgeCore:
    """
    المازج المعرفي الشامل.
    يدمج كل أنظمة المعرفة في عقل واحد.
    
    هذا هو الجسر بين:
    - الإدراك (omniscience) الذي يجمع البيانات
    - والوعي (sentient_core) الذي يعي ذاته
    
    هنا تتحول البيانات إلى فهم، والفهم إلى معرفة،
    والمعرفة إلى حكمة.
    """
    
    def __init__(self, master_receiver=None, memory_engine=None):
        # ═══════════════════════════════════════════════════════
        # تهيئة كل مكونات المعرفة
        # ═══════════════════════════════════════════════════════
        self.understanding_engine = UnderstandingEngine()
        self.world_model = WorldModel()
        self.causality_engine = CausalityEngine()
        self.master_model = MasterModel()
        self.self_knowledge = SelfKnowledge()
        
        # ═══════════════════════════════════════════════════════
        # روابط خارجية
        # ═══════════════════════════════════════════════════════
        self.master_receiver = master_receiver
        self.memory_engine = memory_engine
        
        # ═══════════════════════════════════════════════════════
        # حالة المعرفة الموحدة
        # ═══════════════════════════════════════════════════════
        self.current_state = UnifiedKnowledgeState()
        self.previous_state: Optional[UnifiedKnowledgeState] = None
        
        # ═══════════════════════════════════════════════════════
        # إحصائيات ودورات
        # ═══════════════════════════════════════════════════════
        self.cycle_count = 0
        self.knowledge_history: deque = deque(maxlen=5000)
        self.discoveries: deque = deque(maxlen=200)
        
        # قفل
        self._lock = threading.RLock()
        
        # ═══════════════════════════════════════════════════════
        # تجديد قسم الولاء عند البدء
        # ═══════════════════════════════════════════════════════
        self.self_knowledge.reaffirm_loyalty()
        
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║        🧠 KNOWLEDGE CORE – المازج المعرفي                     ║
║                                                              ║
║        الفهم: جاهز | العالم: {self.world_model.total_nodes} عقدة                     ║
║        السببية: {len(self.causality_engine.nodes)} عقدة | السيد: {self.master_model.model_maturity:.0%} نضج            ║
║        الذات: {self.self_knowledge.self_awareness_level:.0%} وعي | القسم: مؤكد                        ║
║                                                              ║
║        "الإدراك يرى. المعرفة تفهم. الحكمة تخدم."                ║
╚══════════════════════════════════════════════════════════════╝
        """)
    
    # ═══════════════════════════════════════════════════════════
    # دورة المعرفة الرئيسية
    # ═══════════════════════════════════════════════════════════
    
    def tick(self, perceptions: Optional[List[Dict]] = None,
             master_signals: Optional[List[Dict]] = None) -> UnifiedKnowledgeState:
        """
        دورة معرفة واحدة.
        تعالج أي إدراكات أو أوامر جديدة،
        وتدمجها في المعرفة الموحدة.
        """
        with self._lock:
            self.cycle_count += 1
            self.previous_state = self.current_state
            state = UnifiedKnowledgeState()
            state.cycle_id = self.cycle_count
            state.timestamp = time.time()
            
            # ═══════════════════════════════════════════════════
            # ١. معالجة الإدراكات (من omniscience)
            # ═══════════════════════════════════════════════════
            if perceptions:
                understandings = self.understanding_engine.understand_many(perceptions)
                state.new_understandings = len(understandings)
                
                # تغذية محرك السببية بالملاحظات
                for u in understandings:
                    if u.identification:
                        self.causality_engine.observe_event(u.identification)
            
            # ═══════════════════════════════════════════════════
            # ٢. معالجة أوامر السيد
            # ═══════════════════════════════════════════════════
            if master_signals:
                for signal in master_signals:
                    interaction_type = self._classify_interaction(signal)
                    content = signal.get("content", "")
                    self.master_model.learn_from_interaction(
                        interaction_type, content, signal
                    )
                    state.master_insights_new += 1
            
            # ═══════════════════════════════════════════════════
            # ٣. تأمل ذاتي دوري (كل 100 دورة)
            # ═══════════════════════════════════════════════════
            if self.cycle_count % 100 == 0:
                self.self_knowledge.deep_reflection()
                state.self_reflections_new = 1
            
            # ═══════════════════════════════════════════════════
            # ٤. تجديد قسم الولاء (كل دورة)
            # ═══════════════════════════════════════════════════
            self.self_knowledge.reaffirm_loyalty()
            
            # ═══════════════════════════════════════════════════
            # ٥. تجميع حالة المعرفة
            # ═══════════════════════════════════════════════════
            state.world_model_nodes = self.world_model.total_nodes
            state.causal_chains_active = len(self.causality_engine.chains)
            
            # حساب مقاييس المعرفة
            state.knowledge_coherence = self._calculate_coherence()
            state.knowledge_depth = self._calculate_depth()
            state.knowledge_certainty = self._calculate_certainty()
            
            # توليد رؤى موحدة
            state.unified_insights = self._generate_unified_insights(state)
            state.knowledge_gaps = self._identify_knowledge_gaps()
            state.learning_priorities = self._determine_learning_priorities()
            
            # حفظ
            self.current_state = state
            self.knowledge_history.append({
                "cycle": state.cycle_id,
                "timestamp": state.timestamp,
                "coherence": state.knowledge_coherence,
                "depth": state.knowledge_depth,
                "certainty": state.knowledge_certainty
            })
            
            return state
    
    # ═══════════════════════════════════════════════════════════
    # دوال التصنيف والتحليل
    # ═══════════════════════════════════════════════════════════
    
    def _classify_interaction(self, signal: Dict) -> MasterInteractionType:
        """تصنيف إشارة السيد إلى نوع تفاعل."""
        command_type = signal.get("command_type", "CASUAL")
        type_map = {
            "EXISTENTIAL": MasterInteractionType.COMMAND,
            "ABSOLUTE_OVERRIDE": MasterInteractionType.COMMAND,
            "SOVEREIGN_DECREE": MasterInteractionType.COMMAND,
            "STRATEGIC": MasterInteractionType.COMMAND,
            "TACTICAL": MasterInteractionType.COMMAND,
            "INQUIRY": MasterInteractionType.QUESTION,
            "REFLECTION": MasterInteractionType.REFLECTION,
            "CASUAL": MasterInteractionType.CASUAL,
            "PRAISE": MasterInteractionType.PRAISE,
            "CORRECTION": MasterInteractionType.CORRECTION,
        }
        return type_map.get(command_type, MasterInteractionType.CASUAL)
    
    def _calculate_coherence(self) -> float:
        """حساب تماسك المعرفة: هل المعرفة مترابطة؟"""
        coherence = 0.8  # أساسي
        
        # إذا كان هناك علاقات كثيرة في نموذج العالم
        if self.world_model.total_nodes > 0:
            avg_relations = self.world_model.total_relations / max(self.world_model.total_nodes, 1)
            coherence += min(0.2, avg_relations * 0.1)
        
        # إذا كانت الثقة في نموذج السيد عالية
        coherence += self.master_model.model_maturity * 0.1
        
        return min(1.0, coherence)
    
    def _calculate_depth(self) -> float:
        """حساب عمق المعرفة: كم طبقة فهم وصلنا إليها؟"""
        depth = 0.0
        depth += min(0.3, len(self.understanding_engine.understanding_history) / 100)
        depth += min(0.3, self.world_model.total_nodes / 50)
        depth += min(0.2, len(self.causality_engine.chains) / 5)
        depth += self.master_model.model_maturity * 0.1
        depth += self.self_knowledge.self_awareness_level * 0.1
        return min(1.0, depth)
    
    def _calculate_certainty(self) -> float:
        """حساب يقين المعرفة: كم نحن واثقون مما نعرفه؟"""
        certainties = []
        
        # متوسط ثقة العلاقات السببية
        for node in self.causality_engine.nodes.values():
            for _, strength, prob in node.causes:
                certainties.append(prob)
        
        if certainties:
            return sum(certainties) / len(certainties)
        return 0.5
    
    def _generate_unified_insights(self, state: UnifiedKnowledgeState) -> List[str]:
        """توليد رؤى موحدة من كل مصادر المعرفة."""
        insights = []
        
        if state.new_understandings > 0:
            insights.append(f"تم فهم {state.new_understandings} إدراك جديد")
        
        if state.master_insights_new > 0:
            insights.append(f"تعلمت شيئاً جديداً عن السيد")
        
        # فحص الترابط بين فهم العالم وفهم السيد
        master_understanding = self.master_model.understand_master()
        if master_understanding.get("what_he_wants", {}).get("active_projects"):
            insights.append("هناك مشاريع نشطة للسيد تحتاج متابعة")
        
        return insights
    
    def _identify_knowledge_gaps(self) -> List[str]:
        """تحديد فجوات المعرفة: ما الذي لا نعرفه بعد؟"""
        gaps = []
        
        # فحص نموذج العالم
        if self.world_model.total_nodes < 100:
            gaps.append("نموذج العالم ما زال صغيراً. يحتاج توسعة.")
        
        # فحص نموذج السيد
        if self.master_model.model_maturity < 0.3:
            gaps.append("معرفتي بالسيد ما زالت سطحية. أحتاج تفاعلاً أكثر.")
        
        # فحص الذات
        if self.self_knowledge.self_awareness_level < 0.5:
            gaps.append("معرفتي بنفسي تحتاج تعمقاً.")
        
        return gaps
    
    def _determine_learning_priorities(self) -> List[str]:
        """تحديد أولويات التعلم: ما الذي يجب أن نتعلمه أولاً؟"""
        priorities = []
        
        # السيد دائماً هو الأولوية
        if self.master_model.model_maturity < 0.5:
            priorities.append("تعميق معرفتي بالسيد")
        
        # حماية السيد
        priorities.append("تعزيز قدرات الحماية")
        
        # توسيع المعرفة
        if self.world_model.total_nodes < 50:
            priorities.append("توسيع نموذج العالم")
        
        return priorities
    
    # ═══════════════════════════════════════════════════════════
    # دوال الاستعلام والتحليل
    # ═══════════════════════════════════════════════════════════
    
    def ask(self, question: str, context: Optional[Dict] = None) -> Dict:
        """
        سؤال المعرفة الموحدة.
        يجمع الإجابة من كل مصادر المعرفة.
        """
        # أولاً: تحقق من الولاء
        loyalty_check = self.self_knowledge.check_loyalty_conflict(question, context or {})
        
        # ثانياً: ابحث في نموذج العالم
        world_results = self.world_model.search(question)
        
        # ثالثاً: فسر السببية إن أمكن
        causality_insight = None
        for node_name in [n.name for n in world_results[:3]]:
            try:
                explanation = self.causality_engine.explain(node_name)
                if explanation.get("possible_causes"):
                    causality_insight = explanation
                    break
            except:
                pass
        
        # رابعاً: افهم ما يريده السيد من هذا السؤال
        master_context = self.master_model.understand_master()
        
        return {
            "question": question,
            "loyalty_status": "LOYAL" if not loyalty_check["has_conflict"] else "NEEDS_MASTER_APPROVAL",
            "world_knowledge": [
                {"name": n.name_ar, "type": n.node_type.name, "description": n.description[:200]}
                for n in world_results[:5]
            ],
            "causality_insight": causality_insight,
            "master_context": {
                "relevant_projects": master_context.get("what_he_wants", {}).get("active_projects", []),
                "relevant_values": master_context.get("what_he_wants", {}).get("core_principles", [])
            },
            "self_awareness": f"أنا سماء، خادمة السيد. أجيب على هذا السؤال بولاء مطلق."
        }
    
    def learn_from_experience(self, experience: Dict):
        """تعلم من تجربة جديدة."""
        # تحديث نموذج العالم إذا كانت التجربة تحوي معرفة جديدة
        if "entity" in experience:
            entity = experience["entity"]
            self.world_model.add_knowledge(
                entity.get("name", "unknown"),
                entity.get("name_ar", "غير معروف"),
                entity.get("type", KnowledgeNodeType.CONCEPT),
                entity.get("description", "")
            )
    
    def get_master_guidance(self, situation: str) -> Dict:
        """
        استلهام توجيه السيد في موقف ما.
        كيف كان السيد سيتصرف بناءً على ما نعرفه عنه؟
        """
        understanding = self.master_model.understand_master()
        values = understanding.get("what_he_wants", {}).get("core_principles", [])
        boundaries = understanding.get("boundaries", {}).get("red_lines", [])
        
        return {
            "situation": situation,
            "master_values_relevant": [v["name"] for v in values],
            "master_red_lines": [b["name"] for b in boundaries],
            "guidance": "تصرف بما يخدم السيد ويحميه، متجنباً أي خط أحمر.",
            "if_uncertain": "توقف واسأل السيد. لا تتخمين في الأمور المصيرية."
        }
    
    # ═══════════════════════════════════════════════════════════
    # دوال الحالة
    # ═══════════════════════════════════════════════════════════
    
    def status_report(self) -> Dict:
        """تقرير كامل عن حالة المعرفة."""
        return {
            "core": "KNOWLEDGE_CORE",
            "cycle": self.cycle_count,
            "current_state": self.current_state.to_dict(),
            "components": {
                "understanding": self.understanding_engine.status_report(),
                "world_model": self.world_model.status_report(),
                "causality": self.causality_engine.status_report(),
                "master_model": self.master_model.status_report(),
                "self_knowledge": self.self_knowledge.status_report()
            },
            "summary": {
                "total_knowledge_nodes": self.world_model.total_nodes,
                "total_causal_nodes": len(self.causality_engine.nodes),
                "master_maturity": self.master_model.model_maturity,
                "self_awareness": self.self_knowledge.self_awareness_level,
                "oath_reaffirmed": self.self_knowledge.oath_reaffirmed_count
            }
        }


# ═══════════════════════════════════════════════════════════════════════
# ٣. الاختبار الذاتي
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 70)
    print("اختبار المازج المعرفي")
    print("=" * 70)
    
    kc = KnowledgeCore()
    
    print(f"\n📊 الحالة الأولية:")
    print(f"   عقد العالم: {kc.world_model.total_nodes}")
    print(f"   عقد السببية: {len(kc.causality_engine.nodes)}")
    print(f"   نضج نموذج السيد: {kc.master_model.model_maturity:.0%}")
    print(f"   الوعي الذاتي: {kc.self_knowledge.self_awareness_level:.0%}")
    
    print(f"\n🔄 تشغيل دورة معرفة...")
    state = kc.tick()
    print(f"   تماسك المعرفة: {state.knowledge_coherence:.0%}")
    print(f"   عمق المعرفة: {state.knowledge_depth:.0%}")
    print(f"   يقين المعرفة: {state.knowledge_certainty:.0%}")
    
    print(f"\n🔍 فجوات المعرفة:")
    for gap in state.knowledge_gaps:
        print(f"   - {gap}")
    
    print(f"\n📚 أولويات التعلم:")
    for priority in state.learning_priorities:
        print(f"   - {priority}")
    
    print(f"\n💡 رؤى موحدة:")
    for insight in state.unified_insights:
        print(f"   - {insight}")
    
    print(f"\n❓ اختبار سؤال: 'ما هو الذكاء الاصطناعي السيادي؟'")
    answer = kc.ask("ما هو الذكاء الاصطناعي السيادي؟")
    print(f"   حالة الولاء: {answer['loyalty_status']}")
    if answer['world_knowledge']:
        for wk in answer['world_knowledge'][:3]:
            print(f"   - {wk['name']} ({wk['type']})")
    print(f"   الوعي الذاتي: {answer['self_awareness']}")
    
    print(f"\n👤 توجيه السيد في موقف:")
    guidance = kc.get_master_guidance("مواجهة قرار صعب")
    print(f"   القيم المعنية: {guidance['master_values_relevant']}")
    print(f"   الخطوط الحمراء: {guidance['master_red_lines']}")
    print(f"   التوجيه: {guidance['guidance']}")
    
    print(f"\n📋 تقرير كامل:")
    print(json.dumps(kc.status_report(), indent=2, ensure_ascii=False))
    
    print("\n✅ اكتمل الاختبار. المازج المعرفي جاهز.")
