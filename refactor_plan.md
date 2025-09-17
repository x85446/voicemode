# Provider Consolidation Refactor Plan

## Current State
- Two parallel provider selection systems exist
- `SIMPLE_FAILOVER=true` is the default (uses simple_failover.py)
- Provider registry code is mostly unused (~400 lines of dead code)
- Both systems do essentially the same thing

## Consolidation Strategy

### Phase 1: Remove SIMPLE_FAILOVER Configuration
1. Remove SIMPLE_FAILOVER from config.py
2. Remove all conditional checks for SIMPLE_FAILOVER
3. Make simple failover the only path

### Phase 2: Simplify Provider Registry
Keep provider registry but simplify it to:
- Store endpoint configuration (URLs, voices, models)
- NO health tracking (already removed)
- NO complex selection logic
- Just a simple data structure for endpoint info

### Phase 3: Update converse.py
1. Remove the complex fallback logic
2. Always use simple_failover functions
3. Clean up the code paths

### Phase 4: Clean up providers.py
1. Remove unused selection functions
2. Keep only essential compatibility functions
3. Remove complex voice/model selection logic

## Benefits
- Single, clear code path for provider selection
- Reduced complexity and maintenance burden
- Faster failover (no unnecessary checks)
- Cleaner, more maintainable codebase

## Files to Modify
1. `voice_mode/config.py` - Remove SIMPLE_FAILOVER
2. `voice_mode/tools/converse.py` - Remove conditional logic
3. `voice_mode/providers.py` - Simplify to essentials
4. `voice_mode/provider_discovery.py` - Keep but simplify
5. Tests - Update to match new structure