# MCP for Unity - VPM repository

A VPM repository that packages [CoplayDev/unity-mcp](https://github.com/CoplayDev/unity-mcp)
(MCP for Unity, MIT licensed) so it can be added to any Unity project from
**VRChat Creator Companion** or **ALCOM**, with no manual git URLs.

This is an unmodified mirror of the upstream `MCPForUnity` package. All credit goes to
CoplayDev / Coplay.

## Add the repository

Repository URL:

```
https://raw.githubusercontent.com/haroon911/unity-mcp-vpm/main/index.json
```

**One-click: [Add to VCC / ALCOM](https://haroon911.github.io/unity-mcp-vpm/)** (opens a page with an add button; GitHub READMEs can't contain `vcc://` links directly).

Or manually: **Settings -> Packages -> Add Repository**, then paste the URL.

## Use it

1. Open a project in ALCOM / VCC, find **MCP for Unity**, and add it.
2. Open the project in Unity and go to **Window -> MCP for Unity**.
3. Click **Configure All Detected Clients** (this writes your Cursor `mcp.json`).
4. Keep Unity open while using MCP from Cursor.

Requires Unity 2021.3+ and [`uv`](https://docs.astral.sh/uv/) on the machine.

## Updating to a new upstream version

1. Replace the contents of `Packages/com.coplaydev.unity-mcp` with the new upstream `MCPForUnity` folder.
2. Run `python build.py` (writes `dist/*.zip` and updates `index.json`).
3. Commit and push `index.json`, then create a GitHub release tagged `v<version>` and upload `dist/<name>-<version>.zip`.
