from typing import Callable, Dict, Any, List, Optional
from app.rag.vector_store import VectorIndex

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Callable[[str], str]] = {}
        self._descriptions: Dict[str, str] = {}

    def register(self, name: str, description: str, func: Callable[[str], str]) -> None:
        self._tools[name] = func
        self._descriptions[name] = description

    def execute(self, name: str, argument: str) -> str:
        if name not in self._tools:
            return f"Erro: Ferramenta '{name}' não encontrada no registro."
        try:
            return str(self._tools[name](argument))
        except Exception as err:
            return f"Erro na execução da ferramenta {name}: {str(err)}"

    def get_descriptions(self) -> Dict[str, str]:
        return self._descriptions

class ReActAgent:
    def __init__(self, vector_index: Optional[VectorIndex] = None, max_iterations: int = 5):
        self.vector_index = vector_index or VectorIndex()
        self.tools = ToolRegistry()
        self.max_iterations = max_iterations
        self._setup_default_tools()

    def _setup_default_tools(self) -> None:
        # Ferramenta 1: Busca Semântica no RAG
        def search_knowledge(query: str) -> str:
            hits = self.vector_index.search(query, top_k=2)
            if not hits:
                return "Nenhum documento relevante encontrado na base vetorial."
            return " | ".join(f"[{h['doc_id']}]: {h['text']}" for h in hits)

        self.tools.register("search_knowledge", "Pesquisa informações relevantes na base vetorial RAG.", search_knowledge)

        # Ferramenta 2: Calculadora / Estatísticas
        def calculate(expression: str) -> str:
            # Avaliador aritmético determinístico e seguro sem execução dinâmica
            allowed = "0123456789+-*/. "
            if not all(c in allowed for c in expression):
                return "Expressão aritmética não autorizada."
            try:
                tokens = expression.strip().split()
                if len(tokens) == 3:
                    a, op, b = float(tokens[0]), tokens[1], float(tokens[2])
                    if op == "+": return f"Resultado: {a + b}"
                    if op == "-": return f"Resultado: {a - b}"
                    if op == "*": return f"Resultado: {a * b}"
                    if op == "/": return f"Resultado: {a / b if b != 0 else 'divisao por zero'}"
                # Fallback para parsing simples com soma
                numbers = [float(n) for n in expression.replace("+", " ").replace("-", " -").split() if n]
                return f"Resultado: {sum(numbers)}"
            except Exception as e:
                return f"Erro de cálculo: {e}"

        self.tools.register("calculate", "Calcula expressões matemáticas e aritméticas simples.", calculate)

        # Ferramenta 3: Sumarizador de Texto
        def summarize(text: str) -> str:
            words = text.split()
            if len(words) <= 15:
                return text
            return " ".join(words[:15]) + "..."

        self.tools.register("summarize", "Resume e sintetiza trechos de texto longos.", summarize)

    def run(self, user_objective: str) -> Dict[str, Any]:
        trajectory: List[Dict[str, str]] = []
        current_observation = ""

        for step in range(1, self.max_iterations + 1):
            # 1. Thought (Raciocínio)
            if "calcular" in user_objective.lower() or any(op in user_objective for op in ["+", "-", "*", "/"]):
                action = "calculate"
                # Extrai dígitos e operadores
                action_arg = "".join(c for c in user_objective if c in "0123456789+-*/. ")
                thought = f"O usuário precisa de um cálculo. Usarei a ferramenta calculate para: '{action_arg}'."
            elif "buscar" in user_objective.lower() or "pesquisar" in user_objective.lower() or "knowledge" in user_objective.lower():
                action = "search_knowledge"
                action_arg = user_objective
                thought = "O usuário solicitou consulta à base de conhecimento. Executarei busca vetorial."
            else:
                action = "summarize"
                action_arg = user_objective
                thought = "Processarei síntese textual para atender ao objetivo."

            # 2. Action (Execução)
            observation = self.tools.execute(action, action_arg)

            trajectory.append({
                "iteration": str(step),
                "thought": thought,
                "action": action,
                "argument": action_arg,
                "observation": observation
            })

            # Critério de parada / Final Answer
            if observation and not observation.startswith("Erro:"):
                return {
                    "status": "completed",
                    "iterations": step,
                    "final_answer": f"Objetivo atendido: {observation}",
                    "trajectory": trajectory
                }

        return {
            "status": "max_iterations_reached",
            "iterations": self.max_iterations,
            "final_answer": "Limite de iterações do agente atingido.",
            "trajectory": trajectory
        }
