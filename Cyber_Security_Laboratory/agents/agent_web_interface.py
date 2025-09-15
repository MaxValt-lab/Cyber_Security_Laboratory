#!/usr/bin/env python3
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import json
import asyncio
from pathlib import Path
from .code_analyzer_agent import CodeAnalyzerAgent
from .security_scanner_agent import SecurityScannerAgent
from .auto_fixer_agent import AutoFixerAgent

app = FastAPI(title="Agent Control Interface")

class AgentController:
    def __init__(self):
        self.agents = {
            'analyzer': CodeAnalyzerAgent(),
            'security': SecurityScannerAgent(),
            'fixer': AutoFixerAgent()
        }
        self.status = {"running": False, "current_task": None}
    
    async def run_analysis(self, agent_type="all"):
        self.status["running"] = True
        self.status["current_task"] = f"Running {agent_type} analysis"
        
        results = {}
        
        if agent_type in ["all", "analyzer"]:
            self.agents['analyzer'].scan_directory(Path.cwd())
            results['analyzer'] = self.agents['analyzer'].generate_report()
        
        if agent_type in ["all", "security"]:
            self.agents['security'].scan_directory(Path.cwd())
            results['security'] = self.agents['security'].generate_report()
        
        if agent_type in ["all", "fixer"]:
            fixed = self.agents['fixer'].fix_directory(Path.cwd())
            results['fixer'] = {"files_fixed": fixed}
        
        self.status["running"] = False
        self.status["current_task"] = None
        return results

controller = AgentController()

@app.get("/", response_class=HTMLResponse)
def get_interface():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Agent Control Interface</title>
    <style>
        body { font-family: Arial; margin: 20px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; }
        .agent-card { background: white; padding: 20px; margin: 10px 0; border-radius: 8px; }
        .btn { padding: 10px 20px; margin: 5px; border: none; border-radius: 4px; cursor: pointer; }
        .btn-primary { background: #007bff; color: white; }
        .btn-success { background: #28a745; color: white; }
        .btn-warning { background: #ffc107; color: black; }
        .status { padding: 10px; margin: 10px 0; border-radius: 4px; }
        .status.running { background: #fff3cd; }
        .status.idle { background: #d4edda; }
        .results { background: #f8f9fa; padding: 15px; border-radius: 4px; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 Agent Control Interface</h1>
        
        <div id="status" class="status idle">Status: Idle</div>
        
        <div class="agent-card">
            <h3>Code Analysis Agents</h3>
            <button class="btn btn-primary" onclick="runAgent('analyzer')">Run Code Analyzer</button>
            <button class="btn btn-warning" onclick="runAgent('security')">Run Security Scanner</button>
            <button class="btn btn-success" onclick="runAgent('fixer')">Run Auto Fixer</button>
            <button class="btn btn-primary" onclick="runAgent('all')">Run All Agents</button>
        </div>
        
        <div class="agent-card">
            <h3>Agent Status</h3>
            <button class="btn btn-primary" onclick="getStatus()">Get Status</button>
            <button class="btn btn-warning" onclick="stopAgents()">Stop All</button>
        </div>
        
        <div id="results" class="results" style="display:none;">
            <h3>Results</h3>
            <pre id="resultsContent"></pre>
        </div>
    </div>

    <script>
        async function runAgent(type) {
            document.getElementById('status').textContent = 'Status: Running ' + type;
            document.getElementById('status').className = 'status running';
            
            try {
                const response = await fetch('/run-agent/' + type, {method: 'POST'});
                const results = await response.json();
                
                document.getElementById('results').style.display = 'block';
                document.getElementById('resultsContent').textContent = JSON.stringify(results, null, 2);
                
                document.getElementById('status').textContent = 'Status: Completed';
                document.getElementById('status').className = 'status idle';
            } catch (error) {
                alert('Error: ' + error.message);
                document.getElementById('status').textContent = 'Status: Error';
            }
        }
        
        async function getStatus() {
            const response = await fetch('/status');
            const status = await response.json();
            alert('Status: ' + JSON.stringify(status, null, 2));
        }
        
        function stopAgents() {
            alert('Stop functionality not implemented');
        }
    </script>
</body>
</html>
    """

@app.post("/run-agent/{agent_type}")
async def run_agent(agent_type: str):
    if controller.status["running"]:
        raise HTTPException(status_code=400, detail="Agent already running")
    
    results = await controller.run_analysis(agent_type)
    return results

@app.get("/status")
def get_status():
    return controller.status

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)