// Auto-config one-liner for MCP setup
(function() {
  const setups = [
    { name: "Claude Code", path: ".claude/settings.json", key: "settings.json" },
    { name: "OpenCode", path: "opencode.json", key: "opencode.json" },
    { name: "Codex", path: ".codex/config.json", key: "codex" },
    { name: "Cursor", path: ".cursor/mcp.json", key: "cursor" },
    { name: "Windsurf", path: ".windsurf/mcp.json", key: "windsurf" },
    { name: "Continue", path: ".continue/config.json", key: "continue" },
  ];

  window.AITeamHubSetup = {
    detectAgents: function() {
      // Just list all possible — client-side can't read filesystem
      return setups;
    },
    getCommand: function(serverUrl) {
      return `curl -s ${serverUrl}/setup.sh | bash`;
    }
  };
})();
