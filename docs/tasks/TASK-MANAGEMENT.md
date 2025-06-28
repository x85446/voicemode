# Task Management Guidelines

This document describes how to manage tasks, documentation, and specifications in the Voice Mode project.

## Directory Structure

```
docs/
├── tasks/                    # Active development work
│   ├── README.md            # Task list and status
│   ├── archive/             # Completed task documentation
│   ├── implementation-notes.md  # Ongoing implementation decisions
│   ├── key-insights.md      # Important learnings
│   └── [task-name]/         # Task-specific directory
│       ├── README.md        # Task overview and links to all files
│       ├── design.md        # Design and specification (if needed)
│       └── implementation.md # Implementation notes (if needed)
├── specs/                   # Technical specifications
└── [general docs]           # User guides, configuration, etc.
```

## Task Lifecycle

### 1. Creating a New Task
- Add entry to tasks/README.md under appropriate priority section with link to task directory
- Create a dedicated directory for the task: `tasks/[task-name]/`
- Create a README.md in the task directory that includes:
  - Task description and goals
  - Links to all files within the task directory
  - Current status and progress
- For complex tasks, add additional files as needed:
  - `design.md` - Initial design and specification
  - `implementation.md` - Implementation notes and decisions
  - Any other relevant documentation

### 2. Working on Tasks
- Keep all task-related files in the task's directory
- Update the task's README.md with progress and new files
- Update main tasks/README.md status as work progresses
- Document key decisions in the global implementation-notes.md
- Add important learnings to the global key-insights.md

### 3. Completing Tasks
- Move task from active section to "Recently Completed" in README.md
- Include links to relevant documentation
- Extract key insights before archiving

### 4. Archiving Tasks
Archive a task when:
- Implementation is fully complete
- No outstanding issues remain
- All useful information has been extracted

Archive process:
1. Move entire task directory to `archive/` directory
2. Update links in tasks/README.md to point to archived location
3. If design docs are still relevant for future work, consider:
   - Copying them to specs/ directory
   - Creating a summary in specs/ with link to archived task

## Document Types

### Task Documentation
- **Design documents**: Initial planning and specifications
- **Implementation notes**: Decisions made during development
- **Key insights**: Important learnings to preserve

### Specifications (docs/specs/)
- Technical specifications that outlast individual tasks
- Architectural decisions and patterns
- Integration guides and protocols

## Best Practices

### Keep Related Things Together
- During active development, keep specs with their tasks
- Use descriptive filenames that group related documents
- Consider symlinks if documents need to exist in multiple places

### When to Move to specs/
Move documentation to specs/ when:
- It describes a stable, implemented feature
- It provides ongoing architectural guidance
- Multiple future tasks will reference it

### Task README Organization
- **The One Thing**: Single most important current task
- **High Priority**: Critical tasks that block progress
- **Medium Priority**: Important but not blocking
- **Low Priority**: Nice-to-have improvements
- **Ideas to Explore**: Future possibilities
- **Inbox**: New ideas to be triaged
- **Recently Completed**: Finished work with links

### Documentation Updates
- Update CHANGELOG.md when completing user-facing features
- Review and update README.md when archiving tasks
- Keep implementation-notes.md current with decisions

## Examples

### Good Task Organization
```
tasks/
├── provider-registry/
│   ├── README.md            # Overview and links
│   ├── design.md            # Design specification
│   ├── mvp.md              # MVP implementation plan
│   └── implementation.md    # Implementation notes
└── archive/
    └── audio-format-implementation/  # Completed task directory
        ├── README.md
        └── implementation.md
```

### When Not to Archive
- Silence detection: Implementation complete but has known issues
- Provider registry: MVP complete but enhancements ongoing

## Questions to Ask

Before creating a task:
- Is this a bug fix, feature, or improvement?
- What priority level is appropriate?
- Does it need design documentation?

Before archiving:
- Are all issues resolved?
- Has key information been extracted?
- Are there follow-up tasks?

## Future Improvements

- Consider task templates for consistency
- Add task size estimates (S/M/L/XL)
- Track task dependencies
- Add completion dates to archived tasks