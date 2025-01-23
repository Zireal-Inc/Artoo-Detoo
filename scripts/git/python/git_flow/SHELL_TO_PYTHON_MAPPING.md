# Shell Script to Python Implementation Mapping

## Core Functions (gitflow-common -> core.py)

| Shell Function | Python Implementation | Location |
|---------------|----------------------|-----------|
| `warn()` | Logging module | Throughout classes |
| `die()` | Raises `GitFlowError` | Throughout classes |
| `git_local_branches()` | `GitFlow.get_branches()` | core.py |
| `git_remote_branches()` | `GitFlow.get_branches(remote=True)` | core.py |
| `git_current_branch()` | `GitFlow.get_current_branch()` | core.py |
| `git_is_clean_working_tree()` | `GitFlow.is_clean_working_tree()` | core.py |
| `git_do()` | `GitFlow._git_command()` | core.py |
| `gitflow_load_settings()` | `GitFlow._load_settings()` | core.py |

## Feature Commands (git-flow-feature -> commands/feature.py)

| Shell Function | Python Implementation | Location |
|---------------|----------------------|-----------|
| `cmd_start()` | `FeatureCommand.start()` | commands/feature.py |
| `cmd_finish()` | `FeatureCommand.finish()` | commands/feature.py |
| `cmd_publish()` | `FeatureCommand.publish()` | commands/feature.py |
| `cmd_track()` | `FeatureCommand.track()` | commands/feature.py |

## Release Commands (git-flow-release -> commands/release.py)

| Shell Function | Python Implementation | Location |
|---------------|----------------------|-----------|
| `cmd_start()` | `ReleaseCommand.start()` | commands/release.py |
| `cmd_finish()` | `ReleaseCommand.finish()` | commands/release.py |
| `cmd_publish()` | `ReleaseCommand.publish()` | commands/release.py |

## Hotfix Commands (git-flow-hotfix -> commands/hotfix.py)

| Shell Function | Python Implementation | Location |
|---------------|----------------------|-----------|
| `cmd_start()` | `HotfixCommand.start()` | commands/hotfix.py |
| `cmd_finish()` | `HotfixCommand.finish()` | commands/hotfix.py |
| `cmd_publish()` | `HotfixCommand.publish()` | commands/hotfix.py |

## Init Commands (git-flow-init -> commands/init.py)

| Shell Function | Python Implementation | Location |
|---------------|----------------------|-----------|
| `cmd_default()` | `InitCommand.init()` | commands/init.py |
| `git_config_get()` | `GitFlow._git_config_get()` | core.py |
| `git_config_set()` | `GitFlow._git_config_set()` | core.py |

## Key Differences in Implementation

1. **Object-Oriented Approach**: 
   - Python implementation uses classes and inheritance
   - Base functionality in GitFlow class
   - Command-specific code in separate command classes

2. **Error Handling**:
   - Shell: Uses `die()` function with exit codes
   - Python: Uses exceptions (`GitFlowError`)

3. **Command Structure**:
   - Shell: Direct command functions
   - Python: Methods within command classes

4. **Configuration**:
   - Shell: Direct git config calls
   - Python: Wrapped in GitFlow class methods

5. **Branch Management**:
   - Shell: Direct git commands
   - Python: Abstracted methods in GitFlow class

## Note on Implementation Status

Some shell functions are not yet implemented in Python. Planned for future implementation:

- Support for squash merging
- Interactive rebase support
- Remote branch synchronization
- Pull with rebase option
