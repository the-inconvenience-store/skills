# Swarm

How `/implement-spec swarm` runs coding agents in this repo. The orchestrator is the session that invoked it; every other agent is a worker started from the role table below.

## Runtime

- **Multiplexer**: `herdr`
- **Max workers**: `4`
- **Worktree create**: `herdr worktree create --branch <branch> --base <base>`
- **Worktree remove**: `herdr worktree remove --workspace <workspace id>`

Replace the worktree commands with the project's own script when it does setup a bare checkout misses (installing dependencies, copying gitignored fixtures or `.env` files).

## Slot hooks

Optional. Each worker gets a slot number from 1 to max workers. Use it to keep concurrent workers off each other's ports, databases, and profiles where the project allows; anything left out here is shared, and tickets that change a shared resource run one at a time.

- **Env**: `PORT=30{slot}0`
- **Setup**: _(none)_
- **Teardown**: _(none)_

## Roles

`agent` is a herdr agent kind (`herdr agent start --help` lists them). `args` is passed to that agent exactly as written, so put the model and effort flags here in that CLI's own syntax. `notes` goes into each worker's brief for that role.

| Role      | Agent    | Args                       | Notes                                                       |
| --------- | -------- | -------------------------- | ----------------------------------------------------------- |
| `default` | `claude` | `--model opus`             |                                                             |
| `ui`      | `claude` | `--model opus`             | Follow the existing component library and design tokens.    |
| `data`    | `codex`  | `-m <model>`               | Write migrations that are safe to rerun.                    |
| `api`     | `codex`  | `-m <model>`               |                                                             |
| `qa`      | `codex`  | `-m <model>`               | Use a different model from the implementers where possible. |

Every row must name an agent installed on this machine with its herdr integration installed (`herdr integration install <agent>`). `default` and `qa` are required; add or remove the others to match how this project splits work.
