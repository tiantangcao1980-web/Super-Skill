/**
 * Super Skill — AgentAdapter runtime contract (v1).
 *
 * Borrowed from nexu-io/open-design § Agent Adapters. An adapter implements
 * this interface so Super Skill can:
 *   1. detect()           — see if the underlying coding-agent CLI is installed
 *   2. capabilities()     — negotiate streaming / resume / permission policy
 *   3. run(params)        — drive a skill + prompt + working dir, stream events
 *   4. cancel(runId)      — stop a hanging run
 *   5. resume?(runId,msg) — continue an interrupted run
 *
 * Spec: ../../specs/current/agent-adapter-runtime.md
 *
 * This file is the SOURCE OF TRUTH for the v1 shape. The Python protocol
 * mirror lives at scripts/super_skill_adapters/protocol.py and must stay in
 * sync. The audit guard checks the field list at PR time.
 */

export interface AgentDetection {
  /** Absolute path to the CLI executable. */
  executablePath: string;
  /** Whatever the CLI reports for `--version`. */
  version: string;
  /** Per-CLI config directory, e.g. ~/.claude / ~/.codex. */
  configDir?: string;
  /** Per-CLI skills directory the adapter will read/write. */
  skillsDir?: string;
  /** Auth state the adapter could determine. `expired` should trigger UI. */
  authState: "ok" | "missing" | "expired";
}

export interface AgentCapabilities {
  /** Can the agent surgically edit a region of a file without rewriting it. */
  surgicalEdit: boolean;
  /** Does the agent natively load `~/.<agent>/skills/` without a wrapper. */
  nativeSkillLoading: boolean;
  /** Does the agent emit tool calls and text deltas in real time. */
  streaming: boolean;
  /** Can a previously-cancelled run be resumed with `resume()`. */
  resume: boolean;
  /** Permission posture for tool calls. */
  permissionMode: "strict" | "permissive" | "none";
  /** Best-known context-window hint in tokens. */
  contextWindowHint?: number;
}

export interface AgentRunParams {
  /** Unique run id assigned by Super Skill. */
  runId: string;
  /** Absolute path to the artifact / working directory. */
  cwd: string;
  /** Skill body composed for the run (system prompt). */
  systemPrompt: string;
  /** User prompt for the turn. */
  userPrompt: string;
  /** Optional skill folder; the adapter must make these files visible to its CLI. */
  skillDir?: string;
  /** Whitelisted tool ids if the agent supports it. */
  allowedTools?: string[];
  /** Soft wall-clock budget. */
  timeoutMs?: number;
}

export type AgentEvent =
  | { type: "thinking"; text: string }
  | { type: "tool_call"; name: string; input: unknown; id: string }
  | { type: "tool_result"; id: string; output: unknown }
  | { type: "text_delta"; text: string }
  | { type: "file_write"; path: string }
  | { type: "error"; error: string }
  | { type: "done"; reason: "completed" | "cancelled" | "error" };

export interface AgentAdapter {
  readonly id: string;
  readonly displayName: string;

  detect(): Promise<AgentDetection | null>;
  capabilities(): AgentCapabilities;
  run(params: AgentRunParams): AsyncIterable<AgentEvent>;
  cancel(runId: string): Promise<void>;
  resume?(runId: string, message: string): AsyncIterable<AgentEvent>;
}

/**
 * Adapter registry shape returned by `bin/super-skill adapt --runtime <id> --detect-only --json`.
 */
export interface AdapterDetectResult {
  id: string;
  displayName: string;
  detection: AgentDetection | null;
  capabilities: AgentCapabilities;
  recommendation: string;
}
