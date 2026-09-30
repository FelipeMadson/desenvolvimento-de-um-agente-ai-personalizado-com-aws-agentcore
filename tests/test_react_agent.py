import unittest
from app.agents.react_agent import ReActAgent, ToolRegistry

class TestReActAgent(unittest.TestCase):
    def setUp(self):
        self.agent = ReActAgent(max_iterations=3)

    def test_tool_registry_execution(self):
        registry = ToolRegistry()
        registry.register("upper", "Converte para maiúsculas", lambda s: s.upper())
        res = registry.execute("upper", "hello world")
        self.assertEqual(res, "HELLO WORLD")

    def test_agent_calculation_objective(self):
        result = self.agent.run("Por favor, calcular 45 + 55 agora")
        self.assertEqual(result["status"], "completed")
        self.assertIn("100", result["final_answer"])
        self.assertGreater(len(result["trajectory"]), 0)

    def test_agent_summarization(self):
        long_text = "Python é uma linguagem de programação de alto nível, interpretada, de script, imperativa, orientada a objetos e funcional."
        result = self.agent.run(long_text)
        self.assertEqual(result["status"], "completed")
        self.assertIn("Objetivo atendido", result["final_answer"])
