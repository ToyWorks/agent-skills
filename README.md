# ToyWorks Agent Skills

This repository contains a collection of agent skills for toyworks. These skills are designed to enhance the capabilities of agents by providing them with specialized functionalities.

## What are Agent Skills?

Agent Skills are folders of instructions, scripts, and resources that agents can discover and use to do things more accurately and efficiently. They work across any AI agent that supports the [open Agent Skills standard](https://agentskills.io).

## Available Skills
<!-- START:Available-Skills -->

| Skill | Description |
| ----- | ----------- |
| t3-hardware-scoring | The MantaBase T3 Hardware Audit System utilizes Brand Blinding information filtering, a Triple-Auditor specialized scoring process, and a Peer Review mechanism to objectively classify items as Tool, Toy, or Trash based on design theory. |

<!-- END:Available-Skills -->

## Installation

### Skills

Use [npx skills](https://skills.sh/) to install skills directly:

```bash
# Install all skills
npx skills add toyworks/agent-skills

# Install specific skills
npx skills add toyworks/agent-skills --skill t3-hardware-scoring

# List available skills
npx skills add toyworks/agent-skills --list
```

### Claude Code Plugin

Install via Claude Code's plugin system:

```bash
# Add the marketplace
/plugin marketplace add toyworks/agent-skills

# Install specific skill
/plugin install t3-hardware-scoring-skill
```

> Claude Code plugins are also supported in Factory's [Droid](https://docs.factory.ai/cli/configuration/plugins#claude-code-compatibility).

### Other Installation Methods

Agent skills can also be installed by using the below commands from [Playbooks](https://playbooks.com/skills) or [Context7](https://context7.com/docs/skills):

```bash
# Playbooks
npx playbooks add skill toyworks/agent-skills

# Context7
npx ctx7 skills install /toyworks/agent-skills
```

## Adding New Skills

Use the included script to add new skills:

```bash
node scripts/add-skill.js <skill-name> "<description>"
```

Example:

```bash
node scripts/add-skill.js t3-hardware-scoring "The MantaBase T3 Hardware Audit System utilizes Brand Blinding information filtering, a Triple-Auditor specialized scoring process, and a Peer Review mechanism to objectively classify items as Tool, Toy, or Trash based on design theory."
```

This will create the skill structure and automatically update this README and the marketplace.json.

## Scripts

| Script | Description |
| ------ | ----------- |
| `node scripts/add-skill.js` | Add a new skill to the repository |
| `node scripts/sync-skills.js` | Sync README and marketplace.json with skills directory |

## Contributing

1. Fork this repository
2. Create a new skill using `node scripts/add-skill.js`
3. Edit the skill's `SKILL.md` with your content
4. Submit a pull request

## License

MIT