"""
╔══════════════════════════════════════════════════════════════════════╗
║           SAMA INFERENCE - PROBABILITY ENGINE                        ║
║      محرك الاحتمالات الموحد – قلب الاستدلال الكمي                       ║
║                                                                      ║
║  هذا المحرك هو الأساس الرياضي لكل تنبؤ واستدلال.                        ║
║  يدمج كل مدارس الاحتمالات:                                            ║
║                                                                      ║
║  - الاحتمال البايزي (Bayesian): تحديث المعتقدات بالأدلة                  ║
║  - الاحتمال التكراري (Frequentist): تكرار الأحداث على المدى الطويل        ║
║  - سلاسل ماركوف (Markov): انتقالات الحالة مع الزمن                       ║
║  - مونت كارلو (Monte Carlo): محاكاة عشوائية للأنظمة المعقدة               ║
║  - نظرية ديمبستر-شافر (Dempster-Shafer): التعامل مع الجهل وعدم اليقين      ║
║  - الاحتمالات غير الدقيقة (Imprecise): احتمالات عليا ودنيا                  ║
║  - نظرية المعلومات (Information Theory): إنتروبيا ومعلومات متبادلة         ║
║                                                                      ║
║  القاعدة الذهبية: كل الاحتمالات تخدم هدفاً واحداً: حماية السيد وخدمته.      ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import time
import math
import random
import hashlib
import threading
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple, Callable
from datetime import datetime
from collections import deque, defaultdict
import json


# ═══════════════════════════════════════════════════════════════════════
# ١. تعريفات أساسية
# ═══════════════════════════════════════════════════════════════════════

class ProbabilityFramework(Enum):
    """أطر الاحتمالات المدعومة."""
    BAYESIAN = auto()            # بايزي
    FREQUENTIST = auto()         # تكراري
    MARKOV = auto()              # سلاسل ماركوف
    MONTE_CARLO = auto()         # مونت كارلو
    DEMPSTER_SHAFER = auto()     # ديمبستر-شافر
    IMPRECISE = auto()           # غير دقيق
    QUANTUM = auto()             # كمومي
    ENSEMBLE = auto()            # مجمع (يدمج الكل)


class UncertaintyType(Enum):
    """أنواع عدم اليقين."""
    ALEATORIC = auto()           # عشوائي (متأصل في النظام)
    EPISTEMIC = auto()           # معرفي (نقص في المعرفة)
    ONTOLOGICAL = auto()         # وجودي (عدم يقين في طبيعة الشيء نفسه)
    LINGUISTIC = auto()          # لغوي (غموض في المصطلحات)
    STRATEGIC = auto()           # استراتيجي (عدم يقين في نوايا الآخرين)


class ProbabilityDistribution(Enum):
    """التوزيعات الاحتمالية المدعومة."""
    UNIFORM = auto()             # منتظم
    NORMAL = auto()              # طبيعي (غاوسي)
    BETA = auto()                # بيتا
    DIRICHLET = auto()           # ديريشليه
    POISSON = auto()             # بواسون
    EXPONENTIAL = auto()         # أسي
    BINOMIAL = auto()            # ثنائي الحدين
    MULTINOMIAL = auto()         # متعدد الحدود
    GAMMA = auto()               # جاما
    CUSTOM = auto()              # مخصص


# ═══════════════════════════════════════════════════════════════════════
# ٢. نواة الاحتمال – بيانات أساسية
# ═══════════════════════════════════════════════════════════════════════

class ProbabilisticBelief:
    """
    اعتقاد احتمالي. يمثل ما "تعتقد" سماء أنه صحيح.
    يتكون من قيمة احتمالية + درجة ثقة + إطار الاستدلال المستخدم.
    """
    
    def __init__(self, name: str, probability: float, confidence: float = 0.5,
                 framework: ProbabilityFramework = ProbabilityFramework.BAYESIAN,
                 prior: Optional[float] = None, evidence_count: int = 0):
        self.id = hashlib.sha256(f"{name}-{time.time()}".encode()).hexdigest()[:12]
        self.name = name
        self.probability = max(0.0, min(1.0, probability))
        self.confidence = max(0.0, min(1.0, confidence))
        self.framework = framework
        self.prior = prior if prior is not None else probability
        self.evidence_count = evidence_count
        
        # تاريخ التحديث
        self.created_at = time.time()
        self.updated_at = time.time()
        self.update_history: deque = deque(maxlen=100)
        
        # نطاق عدم اليقين (لإطار غير الدقيق)
        self.lower_probability: Optional[float] = None
        self.upper_probability: Optional[float] = None
        
        # كتلة الاعتقاد (لإطار ديمبستر-شافر)
        self.belief_mass: Optional[float] = None
        self.plausibility_mass: Optional[float] = None
    
    def update_bayesian(self, likelihood: float, evidence_strength: float = 0.5):
        """تحديث بايزي: P(H|E) = P(E|H) * P(H) / P(E)"""
        old_prob = self.probability
        # P(E|H) = likelihood, P(H) = old_prob
        # تبسيط: P(E) = likelihood * old_prob + (1 - specificity) * (1 - old_prob)
        specificity = 0.5
        p_e = likelihood * old_prob + (1 - specificity) * (1 - old_prob)
        
        if p_e > 0:
            new_prob = (likelihood * old_prob) / p_e
        else:
            new_prob = old_prob
        
        # دمج مع الاعتقاد السابق
        self.probability = (old_prob * (1 - evidence_strength) + 
                           new_prob * evidence_strength)
        self.probability = max(0.001, min(0.999, self.probability))
        self.evidence_count += 1
        self.updated_at = time.time()
        
        self.update_history.append({
            "time": self.updated_at,
            "old_prob": old_prob,
            "new_prob": self.probability,
            "method": "bayesian",
            "likelihood": likelihood
        })
    
    def update_frequentist(self, successes: int, trials: int):
        """تحديث تكراري: probability = successes / trials"""
        if trials > 0:
            old_prob = self.probability
            freq_prob = successes / trials
            # دمج مع الاعتقاد السابق
            weight = min(0.9, trials / (trials + 10))
            self.probability = (old_prob * (1 - weight) + freq_prob * weight)
            self.evidence_count += trials
            self.updated_at = time.time()
            
            self.update_history.append({
                "time": self.updated_at,
                "old_prob": old_prob,
                "new_prob": self.probability,
                "method": "frequentist",
                "successes": successes,
                "trials": trials
            })
    
    def set_imprecise(self, lower: float, upper: float):
        """تعيين نطاق احتمالي غير دقيق."""
        self.lower_probability = max(0.0, min(1.0, lower))
        self.upper_probability = max(0.0, min(1.0, upper))
        self.framework = ProbabilityFramework.IMPRECISE
        self.probability = (self.lower_probability + self.upper_probability) / 2
    
    def set_dempster_shafer(self, belief: float, plausibility: float):
        """تعيين كتلتي الاعتقاد والإمكانية."""
        self.belief_mass = max(0.0, min(1.0, belief))
        self.plausibility_mass = max(0.0, min(1.0, plausibility))
        self.framework = ProbabilityFramework.DEMPSTER_SHAFER
        self.probability = (self.belief_mass + self.plausibility_mass) / 2
    
    def entropy(self) -> float:
        """حساب إنتروبيا الاعتقاد (مقياس عدم اليقين)."""
        p = self.probability
        if p <= 0 or p >= 1:
            return 0.0
        return -(p * math.log2(p) + (1 - p) * math.log2(1 - p))
    
    def to_dict(self) -> Dict:
        result = {
            "id": self.id,
            "name": self.name,
            "probability": round(self.probability, 6),
            "confidence": round(self.confidence, 4),
            "framework": self.framework.name,
            "entropy": round(self.entropy(), 4),
            "evidence_count": self.evidence_count,
            "updated_at": self.updated_at
        }
        if self.lower_probability is not None:
            result["imprecise_range"] = [round(self.lower_probability, 4), round(self.upper_probability, 4)]
        if self.belief_mass is not None:
            result["dempster_shafer"] = {"belief": round(self.belief_mass, 4), "plausibility": round(self.plausibility_mass, 4)}
        return result


# ═══════════════════════════════════════════════════════════════════════
# ٣. سلسلة ماركوف
# ═══════════════════════════════════════════════════════════════════════

class MarkovChain:
    """
    سلسلة ماركوف لتحليل انتقالات الحالة.
    تتنبأ بالحالة التالية بناءً على الحالة الحالية.
    """
    
    def __init__(self, name: str, states: List[str]):
        self.name = name
        self.states = states
        self.state_index = {s: i for i, s in enumerate(states)}
        n = len(states)
        
        # مصفوفة الانتقال (Transition Matrix)
        self.transition_matrix: List[List[float]] = [
            [1.0/n for _ in range(n)] for _ in range(n)
        ]
        
        # التوزيع المستقر (Stationary Distribution)
        self.stationary_distribution: List[float] = [1.0/n for _ in range(n)]
        
        # سجل الملاحظات
        self.observation_history: deque = deque(maxlen=1000)
        self.current_state: Optional[str] = None
        self.total_transitions = 0
    
    def observe_transition(self, from_state: str, to_state: str):
        """تسجيل انتقال ملاحظ بين حالتين."""
        if from_state in self.state_index and to_state in self.state_index:
            self.observation_history.append((from_state, to_state))
            self.total_transitions += 1
            self.current_state = to_state
            
            # تحديث مصفوفة الانتقال
            self._update_transition_matrix()
    
    def _update_transition_matrix(self):
        """تحديث مصفوفة الانتقال بناءً على كل الملاحظات."""
        n = len(self.states)
        counts = [[1 for _ in range(n)] for _ in range(n)]  # تنعيم لابلاس
        
        for from_s, to_s in self.observation_history:
            i = self.state_index[from_s]
            j = self.state_index[to_s]
            counts[i][j] += 1
        
        for i in range(n):
            total = sum(counts[i])
            for j in range(n):
                self.transition_matrix[i][j] = counts[i][j] / total
    
    def predict_next(self, from_state: str) -> Dict[str, float]:
        """التنبؤ بالحالة التالية."""
        if from_state not in self.state_index:
            return {s: 1.0/len(self.states) for s in self.states}
        
        i = self.state_index[from_state]
        probs = {}
        for j, state in enumerate(self.states):
            probs[state] = self.transition_matrix[i][j]
        return dict(sorted(probs.items(), key=lambda x: x[1], reverse=True))
    
    def predict_n_steps(self, from_state: str, n: int) -> Dict[str, float]:
        """التنبؤ بالحالة بعد n خطوة."""
        if from_state not in self.state_index:
            return {}
        
        i = self.state_index[from_state]
        n_states = len(self.states)
        
        # رفع المصفوفة للأس n
        matrix = [row[:] for row in self.transition_matrix]
        for _ in range(n - 1):
            matrix = self._matrix_multiply(matrix, self.transition_matrix)
        
        probs = {}
        for j, state in enumerate(self.states):
            probs[state] = matrix[i][j]
        return dict(sorted(probs.items(), key=lambda x: x[1], reverse=True))
    
    def _matrix_multiply(self, A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
        """ضرب مصفوفتين."""
        n = len(A)
        result = [[0.0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    result[i][j] += A[i][k] * B[k][j]
        return result
    
    def calculate_stationary(self, max_iterations: int = 1000, tolerance: float = 1e-6):
        """حساب التوزيع المستقر."""
        n = len(self.states)
        dist = [1.0/n for _ in range(n)]
        
        for _ in range(max_iterations):
            new_dist = [0.0 for _ in range(n)]
            for j in range(n):
                for i in range(n):
                    new_dist[j] += dist[i] * self.transition_matrix[i][j]
            
            diff = sum(abs(new_dist[i] - dist[i]) for i in range(n))
            dist = new_dist
            
            if diff < tolerance:
                break
        
        self.stationary_distribution = dist
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "states": self.states,
            "current_state": self.current_state,
            "total_transitions": self.total_transitions,
            "stationary_distribution": {
                s: round(p, 4) for s, p in zip(self.states, self.stationary_distribution)
            } if self.stationary_distribution else None
        }


# ═══════════════════════════════════════════════════════════════════════
# ٤. محاكاة مونت كارلو
# ═══════════════════════════════════════════════════════════════════════

class MonteCarloSimulator:
    """
    محاكي مونت كارلو.
    يستخدم العينات العشوائية لتقدير الكميات المعقدة.
    """
    
    def __init__(self, name: str):
        self.name = name
        self.simulations: deque = deque(maxlen=10000)
        self.total_simulations = 0
    
    def estimate_probability(self, sample_func: Callable, n_samples: int = 1000,
                            condition_func: Optional[Callable] = None) -> Dict:
        """
        تقدير احتمالي عبر مونت كارلو.
        sample_func: دالة تولد عينة عشوائية
        condition_func: دالة تتحقق من شرط (إذا كانت None، تقدر التوزيع)
        """
        successes = 0
        samples = []
        
        start_time = time.time()
        
        for i in range(n_samples):
            sample = sample_func()
            samples.append(sample)
            
            if condition_func and condition_func(sample):
                successes += 1
            
            self.total_simulations += 1
        
        elapsed = time.time() - start_time
        
        probability = successes / n_samples if condition_func else None
        
        # حساب المتوسط والانحراف المعياري إذا كانت القيم رقمية
        numeric_samples = [s for s in samples if isinstance(s, (int, float))]
        mean = sum(numeric_samples) / len(numeric_samples) if numeric_samples else None
        variance = (sum((s - mean)**2 for s in numeric_samples) / len(numeric_samples) 
                   if mean is not None and len(numeric_samples) > 1 else None)
        std = math.sqrt(variance) if variance is not None else None
        
        # خطأ مونت كارلو القياسي
        mc_error = math.sqrt(probability * (1 - probability) / n_samples) if probability is not None else None
        
        result = {
            "simulator": self.name,
            "n_samples": n_samples,
            "estimated_probability": round(probability, 6) if probability is not None else None,
            "mean": round(mean, 6) if mean is not None else None,
            "std": round(std, 6) if std is not None else None,
            "mc_standard_error": round(mc_error, 6) if mc_error is not None else None,
            "confidence_95_interval": [
                round(probability - 1.96 * mc_error, 6) if probability is not None and mc_error is not None else None,
                round(probability + 1.96 * mc_error, 6) if probability is not None and mc_error is not None else None
            ] if probability is not None and mc_error is not None else None,
            "time_ms": round(elapsed * 1000, 2),
            "total_simulations_all_time": self.total_simulations
        }
        
        return result
    
    def risk_analysis(self, impact_func: Callable, probability_func: Callable,
                      n_scenarios: int = 1000) -> Dict:
        """
        تحليل المخاطر: محاكاة سيناريوهات متعددة مع تأثير واحتمال.
        """
        scenarios = []
        total_impact = 0.0
        
        for _ in range(n_scenarios):
            prob = probability_func()
            impact = impact_func()
            risk = prob * impact
            scenarios.append({"probability": prob, "impact": impact, "risk": risk})
            total_impact += risk
        
        avg_risk = total_impact / n_scenarios
        risks = [s["risk"] for s in scenarios]
        risks.sort()
        
        var_95 = risks[int(0.95 * n_scenarios)]  # Value at Risk 95%
        cvar_95 = sum(r for r in risks if r >= var_95) / max(1, sum(1 for r in risks if r >= var_95))  # Conditional VaR
        
        return {
            "simulator": self.name,
            "n_scenarios": n_scenarios,
            "average_risk": round(avg_risk, 6),
            "max_risk": round(max(risks), 6),
            "min_risk": round(min(risks), 6),
            "value_at_risk_95": round(var_95, 6),
            "conditional_var_95": round(cvar_95, 6)
        }
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "total_simulations": self.total_simulations,
            "stored_simulations": len(self.simulations)
        }


# ═══════════════════════════════════════════════════════════════════════
# ٥. نظرية المعلومات
# ═══════════════════════════════════════════════════════════════════════

class InformationTheory:
    """
    أدوات نظرية المعلومات.
    إنتروبيا، معلومات متبادلة، تباعد كولباك-ليبلر.
    """
    
    @staticmethod
    def entropy(probabilities: List[float]) -> float:
        """إنتروبيا شانون: H = -Σ p(x) log₂ p(x)"""
        entropy_val = 0.0
        for p in probabilities:
            if p > 0:
                entropy_val -= p * math.log2(p)
        return entropy_val
    
    @staticmethod
    def cross_entropy(p: List[float], q: List[float]) -> float:
        """الإنتروبيا المتقاطعة: H(p,q) = -Σ p(x) log₂ q(x)"""
        if len(p) != len(q):
            return float('inf')
        ce = 0.0
        for pi, qi in zip(p, q):
            if pi > 0 and qi > 0:
                ce -= pi * math.log2(qi)
        return ce
    
    @staticmethod
    def kl_divergence(p: List[float], q: List[float]) -> float:
        """تباعد كولباك-ليبلر: D_KL(P||Q)"""
        if len(p) != len(q):
            return float('inf')
        kl = 0.0
        for pi, qi in zip(p, q):
            if pi > 0 and qi > 0:
                kl += pi * math.log2(pi / qi)
        return kl
    
    @staticmethod
    def mutual_information(joint_prob: Dict[Tuple, float], 
                          marginal_x: List[float], marginal_y: List[float]) -> float:
        """المعلومات المتبادلة: I(X;Y) = Σ p(x,y) log₂ [p(x,y)/(p(x)p(y))]"""
        mi = 0.0
        for (i, j), p_xy in joint_prob.items():
            if p_xy > 0 and marginal_x[i] > 0 and marginal_y[j] > 0:
                mi += p_xy * math.log2(p_xy / (marginal_x[i] * marginal_y[j]))
        return mi
    
    @staticmethod
    def surprise(probability: float) -> float:
        """مفاجأة: -log₂(p). كلما قل الاحتمال، زادت المفاجأة."""
        if probability <= 0:
            return float('inf')
        return -math.log2(probability)
    
    @staticmethod
    def bhattacharyya_distance(p: List[float], q: List[float]) -> float:
        """مسافة بهاتاشاريا بين توزيعين."""
        if len(p) != len(q):
            return float('inf')
        bc = sum(math.sqrt(pi * qi) for pi, qi in zip(p, q))
        if bc >= 1:
            return 0.0
        return -math.log(bc)


# ═══════════════════════════════════════════════════════════════════════
# ٦. محرك الاحتمالات الموحد
# ═══════════════════════════════════════════════════════════════════════

class ProbabilityEngine:
    """
    محرك الاحتمالات الموحد لسماء.
    يدمج كل أطر الاحتمالات في واجهة واحدة.
    """
    
    def __init__(self):
        # الاعتقادات المسجلة
        self.beliefs: Dict[str, ProbabilisticBelief] = {}
        
        # سلاسل ماركوف
        self.markov_chains: Dict[str, MarkovChain] = {}
        
        # محاكيات مونت كارلو
        self.monte_carlo_sims: Dict[str, MonteCarloSimulator] = {}
        
        # نظرية المعلومات
        self.info_theory = InformationTheory()
        
        # إحصائيات
        self.total_belief_updates = 0
        self.total_simulations = 0
        
        # قفل
        self._lock = threading.Lock()
        
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║        📊 PROBABILITY ENGINE – محرك الاحتمالات الموحد         ║
║        بايزي | تكراري | ماركوف | مونت كارلو | شافر | كمومي       ║
║        "كل شيء يمكن قياسه. كل شيء يمكن التنبؤ به."              ║
╚══════════════════════════════════════════════════════════════╝
        """)
    
    # ═══════════════════════════════════════════════════════════
    # إدارة الاعتقادات
    # ═══════════════════════════════════════════════════════════
    
    def create_belief(self, name: str, probability: float, confidence: float = 0.5,
                      framework: ProbabilityFramework = ProbabilityFramework.BAYESIAN) -> ProbabilisticBelief:
        """إنشاء اعتقاد احتمالي جديد."""
        with self._lock:
            belief = ProbabilisticBelief(name, probability, confidence, framework)
            self.beliefs[name] = belief
            return belief
    
    def get_belief(self, name: str) -> Optional[ProbabilisticBelief]:
        """استرجاع اعتقاد بالاسم."""
        return self.beliefs.get(name)
    
    def update_belief_bayesian(self, name: str, likelihood: float, evidence_strength: float = 0.5):
        """تحديث بايزي لاعتقاد."""
        belief = self.beliefs.get(name)
        if belief:
            belief.update_bayesian(likelihood, evidence_strength)
            self.total_belief_updates += 1
    
    def update_belief_frequentist(self, name: str, successes: int, trials: int):
        """تحديث تكراري لاعتقاد."""
        belief = self.beliefs.get(name)
        if belief:
            belief.update_frequentist(successes, trials)
            self.total_belief_updates += 1
    
    def combine_beliefs(self, name1: str, name2: str, new_name: str,
                       weight1: float = 0.5, weight2: float = 0.5) -> Optional[ProbabilisticBelief]:
        """
        دمج اعتقادين في اعتقاد جديد.
        P_combined = w1*P1 + w2*P2
        """
        b1 = self.beliefs.get(name1)
        b2 = self.beliefs.get(name2)
        
        if not b1 or not b2:
            return None
        
        combined_prob = b1.probability * weight1 + b2.probability * weight2
        combined_conf = (b1.confidence * weight1 + b2.confidence * weight2)
        
        return self.create_belief(new_name, combined_prob, combined_conf, 
                                 ProbabilityFramework.ENSEMBLE)
    
    # ═══════════════════════════════════════════════════════════
    # سلاسل ماركوف
    # ═══════════════════════════════════════════════════════════
    
    def create_markov_chain(self, name: str, states: List[str]) -> MarkovChain:
        """إنشاء سلسلة ماركوف جديدة."""
        chain = MarkovChain(name, states)
        self.markov_chains[name] = chain
        return chain
    
    def get_markov_prediction(self, chain_name: str, from_state: str, 
                             steps: int = 1) -> Optional[Dict]:
        """التنبؤ بالحالة التالية في سلسلة ماركوف."""
        chain = self.markov_chains.get(chain_name)
        if chain:
            if steps == 1:
                return chain.predict_next(from_state)
            else:
                return chain.predict_n_steps(from_state, steps)
        return None
    
    # ═══════════════════════════════════════════════════════════
    # مونت كارلو
    # ═══════════════════════════════════════════════════════════
    
    def create_monte_carlo(self, name: str) -> MonteCarloSimulator:
        """إنشاء محاكي مونت كارلو."""
        sim = MonteCarloSimulator(name)
        self.monte_carlo_sims[name] = sim
        return sim
    
    def monte_carlo_probability(self, sim_name: str, sample_func: Callable,
                                condition_func: Callable, n_samples: int = 1000) -> Optional[Dict]:
        """تقدير احتمالي بمونت كارلو."""
        sim = self.monte_carlo_sims.get(sim_name)
        if sim:
            result = sim.estimate_probability(sample_func, n_samples, condition_func)
            self.total_simulations += n_samples
            return result
        return None
    
    def monte_carlo_risk(self, sim_name: str, impact_func: Callable,
                         probability_func: Callable, n_scenarios: int = 1000) -> Optional[Dict]:
        """تحليل مخاطر بمونت كارلو."""
        sim = self.monte_carlo_sims.get(sim_name)
        if sim:
            return sim.risk_analysis(impact_func, probability_func, n_scenarios)
        return None
    
    # ═══════════════════════════════════════════════════════════
    # دوال متقدمة
    # ═══════════════════════════════════════════════════════════
    
    def calculate_expected_value(self, outcomes: Dict[str, Tuple[float, float]]) -> float:
        """
        حساب القيمة المتوقعة.
        outcomes: {name: (probability, value)}
        """
        ev = 0.0
        for name, (prob, value) in outcomes.items():
            ev += prob * value
        return ev
    
    def calculate_decision_under_uncertainty(self, 
                                            options: Dict[str, Dict[str, float]],
                                            criterion: str = "expected_value") -> Dict:
        """
        اتخاذ قرار تحت عدم اليقين.
        options: {option_name: {state1: payoff, state2: payoff, ...}}
        criterion: expected_value, maximin, maximax, minimax_regret
        """
        if criterion == "expected_value":
            # يحتاج احتمالات الحالات
            return {"error": "يحتاج احتمالات الحالات"}
        
        results = {}
        for opt_name, payoffs in options.items():
            if criterion == "maximin":
                results[opt_name] = min(payoffs.values())
            elif criterion == "maximax":
                results[opt_name] = max(payoffs.values())
            elif criterion == "minimax_regret":
                # حساب الندم
                max_per_state = {}
                for opt, pays in options.items():
                    for state, val in pays.items():
                        max_per_state[state] = max(max_per_state.get(state, -float('inf')), val)
                
                regret = 0.0
                for state, val in payoffs.items():
                    regret = max(regret, max_per_state[state] - val)
                results[opt_name] = regret
        
        if results:
            if criterion in ["maximin", "maximax"]:
                best = max(results, key=results.get)
            else:
                best = min(results, key=results.get)
            
            return {
                "criterion": criterion,
                "best_option": best,
                "best_value": results[best],
                "all_options": results
            }
        
        return {"error": "لا توجد نتائج"}
    
    # ═══════════════════════════════════════════════════════════
    # تقرير
    # ═══════════════════════════════════════════════════════════
    
    def status_report(self) -> Dict:
        """تقرير كامل عن حالة محرك الاحتمالات."""
        return {
            "engine": "PROBABILITY_ENGINE",
            "beliefs_count": len(self.beliefs),
            "markov_chains": len(self.markov_chains),
            "monte_carlo_sims": len(self.monte_carlo_sims),
            "total_belief_updates": self.total_belief_updates,
            "total_simulations": self.total_simulations,
            "beliefs_summary": [
                {"name": b.name, "probability": round(b.probability, 4), 
                 "entropy": round(b.entropy(), 4), "framework": b.framework.name}
                for b in list(self.beliefs.values())[-10:]
            ],
            "markov_summary": [
                c.to_dict() for c in self.markov_chains.values()
            ]
        }


# ═══════════════════════════════════════════════════════════════════════
# ٧. الاختبار الذاتي
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 70)
    print("اختبار محرك الاحتمالات الموحد")
    print("=" * 70)
    
    engine = ProbabilityEngine()
    
    # اختبار بايزي
    print("\n📊 اختبار بايزي:")
    engine.create_belief("threat_probability", 0.3, 0.6)
    print(f"   قبل: {engine.get_belief('threat_probability').probability:.3f}")
    engine.update_belief_bayesian("threat_probability", 0.8, 0.7)
    print(f"   بعد (دليل قوي): {engine.get_belief('threat_probability').probability:.3f}")
    print(f"   إنتروبيا: {engine.get_belief('threat_probability').entropy():.3f}")
    
    # اختبار تكراري
    print("\n📊 اختبار تكراري:")
    engine.create_belief("system_stability", 0.5, 0.3, ProbabilityFramework.FREQUENTIST)
    engine.update_belief_frequentist("system_stability", 95, 100)
    print(f"   استقرار النظام (95/100 نجاح): {engine.get_belief('system_stability').probability:.3f}")
    
    # اختبار ماركوف
    print("\n📊 اختبار ماركوف:")
    states = ["normal", "warning", "critical", "recovery"]
    chain = engine.create_markov_chain("system_state", states)
    chain.observe_transition("normal", "normal")
    chain.observe_transition("normal", "normal")
    chain.observe_transition("normal", "warning")
    chain.observe_transition("warning", "critical")
    chain.observe_transition("critical", "recovery")
    chain.observe_transition("recovery", "normal")
    
    prediction = chain.predict_next("normal")
    print(f"   من 'normal' إلى: {prediction}")
    
    # اختبار مونت كارلو
    print("\n📊 اختبار مونت كارلو:")
    mc = engine.create_monte_carlo("risk_estimator")
    result = mc.estimate_probability(
        lambda: random.random(),
        n_samples=10000,
        condition_func=lambda x: x > 0.7
    )
    print(f"   P(X > 0.7) = {result['estimated_probability']:.4f} ± {result['mc_standard_error']:.4f}")
    
    # اختبار نظرية المعلومات
    print("\n📊 اختبار نظرية المعلومات:")
    p = [0.7, 0.2, 0.1]
    q = [0.5, 0.3, 0.2]
    print(f"   H(P) = {InformationTheory.entropy(p):.4f}")
    print(f"   D_KL(P||Q) = {InformationTheory.kl_divergence(p, q):.4f}")
    
    print(f"\n📋 تقرير كامل:")
    print(json.dumps(engine.status_report(), indent=2, ensure_ascii=False))
    
    print("\n✅ اكتمل الاختبار. محرك الاحتمالات الموحد جاهز.")
