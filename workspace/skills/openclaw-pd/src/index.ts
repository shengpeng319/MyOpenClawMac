import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
import { Type } from "@sinclair/typebox";
import { readFileSync, readdirSync, existsSync } from "fs";
import { join, basename } from "path";

const SKILLS_DIR = join(process.env.HOME || "/Users/shengpeng319", ".openclaw/workspace/skills");

interface SkillIndex {
  name: string;
  description: string;
  category: string;
  hasL2: boolean;
}

function getL0Skills(): SkillIndex[] {
  const skills: SkillIndex[] = [];
  
  if (!existsSync(SKILLS_DIR)) {
    return skills;
  }
  
  const entries = readdirSync(SKILLS_DIR, { withFileTypes: true });
  
  for (const entry of entries) {
    if (!entry.isDirectory() || entry.name.startsWith(".")) continue;
    
    const skillPath = join(SKILLS_DIR, entry.name);
    const skillMdPath = join(skillPath, "SKILL.md");
    
    if (!existsSync(skillMdPath)) continue;
    
    // Read first 2KB of SKILL.md for description
    let description = "";
    try {
      const content = readFileSync(skillMdPath, "utf-8");
      const lines = content.split("\n").slice(0, 20);
      for (const line of lines) {
        if (line.startsWith("description:") || line.startsWith("description =")) {
          description = line.replace(/^description:?\s*/, "").replace(/^description = \"/, "").replace(/"/g, "").trim();
          break;
        }
      }
      if (!description && lines.length > 2) {
        description = lines.slice(2).join(" ").replace(/^#.*$/, "").trim().slice(0, 200);
      }
    } catch {}
    
    // Check for references/ subdirectory (L2)
    const refsPath = join(skillPath, "references");
    const hasL2 = existsSync(refsPath);
    
    // Determine category from path or name
    let category = "general";
    if (entry.name.includes("marketing")) category = "marketing";
    else if (entry.name.includes("stock")) category = "finance";
    else if (entry.name.includes("web") || entry.name.includes("reach")) category = "web";
    else if (entry.name.includes("coding") || entry.name.includes("code")) category = "coding";
    else if (entry.name.includes("self-improving")) category = "agent";
    
    skills.push({
      name: entry.name,
      description: description.slice(0, 300),
      category,
      hasL2,
    });
  }
  
  return skills.sort((a, b) => a.name.localeCompare(b.name));
}

function loadSkill(name: string, filePath?: string): string {
  const skillPath = join(SKILLS_DIR, name);
  const skillMdPath = join(skillPath, "SKILL.md");
  
  if (!existsSync(skillMdPath)) {
    return JSON.stringify({ error: `Skill '${name}' not found` });
  }
  
  // L1: return full SKILL.md
  if (!filePath) {
    try {
      return readFileSync(skillMdPath, "utf-8");
    } catch {
      return JSON.stringify({ error: `Failed to read SKILL.md for '${name}'` });
    }
  }
  
  // L2: return specific file from references/
  const refsPath = join(skillPath, "references", filePath);
  
  if (!existsSync(refsPath)) {
    return JSON.stringify({ error: `File '${filePath}' not found in '${name}' references/` });
  }
  
  try {
    return readFileSync(refsPath, "utf-8");
  } catch {
    return JSON.stringify({ error: `Failed to read '${filePath}' in '${name}'` });
  }
}

export default definePluginEntry({
  id: "openclaw-pd",
  name: "Progressive Disclosure",
  description: "Provides skills_list and skill_view tools for L0/L1/L2 progressive skill loading",
  register(api) {
    // L0: List all skills (index)
    api.registerTool({
      name: "skills_list",
      description: "List all available skills (L0 index). Returns name, description, category, and hasL2 flag for each skill. Use this to discover available skills before loading specific ones.",
      parameters: Type.Object({}),
      async execute(_id, _params) {
        const skills = getL0Skills();
        return {
          content: [{
            type: "text" as const,
            text: JSON.stringify({ skills }, null, 2),
          }],
        };
      },
    });

    // L1: Load full SKILL.md, L2: Load specific file
    api.registerTool({
      name: "skill_view",
      description: "Load skill content. Without path: returns full SKILL.md (L1). With path: returns specific file from references/ subdirectory (L2).",
      parameters: Type.Object({
        name: Type.String({ description: "Skill directory name" }),
        path: Type.Optional(Type.String({ description: "File path within references/ subdirectory (L2)" })),
      }),
      async execute(_id, params) {
        const content = loadSkill(params.name, params.path);
        return {
          content: [{ type: "text" as const, text: content }],
        };
      },
    });
  },
});
