#!/bin/bash
# Bash completion for voicemode command
# Source this file or place in /etc/bash_completion.d/

_voicemode_complete() {
    local cur prev words cword
    _init_completion || return

    # Main command groups
    local main_commands="kokoro whisper livekit config diag exchanges --version --help -h"
    
    # Service commands (common to kokoro, whisper, livekit)
    local service_commands="status start stop restart enable disable logs update-service-files health install uninstall"
    
    # Whisper models
    local whisper_models="tiny tiny.en base base.en small small.en medium medium.en large-v1 large-v2 large-v3 large-v3-turbo"
    
    # Whisper model commands
    local whisper_model_commands="install remove"
    
    # Config commands
    local config_commands="list get set"
    
    # Diagnostic commands
    local diag_commands="info devices registry dependencies"
    
    # Exchanges commands
    local exchanges_commands="tail view search stats export"
    
    # LiveKit-specific commands (includes frontend subgroup)
    local livekit_commands="$service_commands frontend"
    
    # Frontend commands
    local frontend_commands="install start stop status open logs enable disable build"
    
    # Install options (common to all services)
    local install_opts="--install-dir --port --force --version --auto-enable --no-auto-enable"
    
    # Uninstall options (common to all services)
    local uninstall_opts="--remove-models --remove-all-data"
    
    # Format options for exchanges
    local format_opts="simple pretty json raw csv markdown html"
    
    # Transport options
    local transport_opts="local livekit speak-only all"
    
    # Exchange types
    local exchange_types="stt tts all"

    case ${words[1]} in
        kokoro)
            case ${words[2]} in
                install)
                    case $prev in
                        --install-dir)
                            _filedir -d
                            return
                            ;;
                        --port)
                            COMPREPLY=($(compgen -W "8880 8881 8882" -- "$cur"))
                            return
                            ;;
                        --version)
                            COMPREPLY=($(compgen -W "latest v1.0.0" -- "$cur"))
                            return
                            ;;
                        *)
                            COMPREPLY=($(compgen -W "$install_opts -f -h --help" -- "$cur"))
                            return
                            ;;
                    esac
                    ;;
                uninstall)
                    COMPREPLY=($(compgen -W "$uninstall_opts --help -h" -- "$cur"))
                    return
                    ;;
                logs)
                    case $prev in
                        --lines|-n)
                            COMPREPLY=($(compgen -W "10 20 50 100 500" -- "$cur"))
                            return
                            ;;
                        *)
                            COMPREPLY=($(compgen -W "--lines -n --help -h" -- "$cur"))
                            return
                            ;;
                    esac
                    ;;
                *)
                    # Add 'models' and 'model' to the service commands for whisper
                    COMPREPLY=($(compgen -W "$service_commands models model download-model" -- "$cur"))
                    return
                    ;;
            esac
            ;;
            
        whisper)
            case ${words[2]} in
                model)
                    # Handle 'whisper model' subcommands
                    case ${words[3]} in
                        install)
                            # Complete model names for install
                            if [[ $prev == "install" ]]; then
                                COMPREPLY=($(compgen -W "$whisper_models all" -- "$cur"))
                            else
                                COMPREPLY=($(compgen -W "--force -f --skip-core-ml --help -h" -- "$cur"))
                            fi
                            return
                            ;;
                        remove)
                            # Complete model names for remove
                            if [[ $prev == "remove" ]]; then
                                COMPREPLY=($(compgen -W "$whisper_models" -- "$cur"))
                            else
                                COMPREPLY=($(compgen -W "--force -f --help -h" -- "$cur"))
                            fi
                            return
                            ;;
                        "")
                            # Complete model names for setting or subcommands
                            COMPREPLY=($(compgen -W "$whisper_models $whisper_model_commands --help -h" -- "$cur"))
                            return
                            ;;
                        *)
                            # If a model name was given, no more completions
                            if [[ " $whisper_models " =~ " ${words[3]} " ]]; then
                                return
                            fi
                            COMPREPLY=($(compgen -W "$whisper_model_commands --help -h" -- "$cur"))
                            return
                            ;;
                    esac
                    ;;
                models)
                    # No arguments for 'whisper models'
                    COMPREPLY=($(compgen -W "--help -h" -- "$cur"))
                    return
                    ;;
                install)
                    case $prev in
                        --install-dir)
                            _filedir -d
                            return
                            ;;
                        --model)
                            COMPREPLY=($(compgen -W "tiny tiny.en base base.en small small.en medium medium.en large-v1 large-v2 large-v3 large-v3-turbo" -- "$cur"))
                            return
                            ;;
                        --version)
                            COMPREPLY=($(compgen -W "latest v1.0.0" -- "$cur"))
                            return
                            ;;
                        *)
                            COMPREPLY=($(compgen -W "$install_opts --model --use-gpu --no-gpu -f --help -h" -- "$cur"))
                            return
                            ;;
                    esac
                    ;;
                uninstall)
                    COMPREPLY=($(compgen -W "$uninstall_opts --help -h" -- "$cur"))
                    return
                    ;;
                # Keep download-model for backwards compatibility
                download-model)
                    case $prev in
                        download-model)
                            COMPREPLY=($(compgen -W "$whisper_models all" -- "$cur"))
                            return
                            ;;
                        *)
                            COMPREPLY=($(compgen -W "--force -f --skip-core-ml --help -h" -- "$cur"))
                            return
                            ;;
                    esac
                    ;;
                logs)
                    case $prev in
                        --lines|-n)
                            COMPREPLY=($(compgen -W "10 20 50 100 500" -- "$cur"))
                            return
                            ;;
                        *)
                            COMPREPLY=($(compgen -W "--lines -n --help -h" -- "$cur"))
                            return
                            ;;
                    esac
                    ;;
                *)
                    COMPREPLY=($(compgen -W "$service_commands download-model" -- "$cur"))
                    return
                    ;;
            esac
            ;;
            
        livekit)
            case ${words[2]} in
                install)
                    case $prev in
                        --install-dir)
                            _filedir -d
                            return
                            ;;
                        --port)
                            COMPREPLY=($(compgen -W "7880 7881 7882" -- "$cur"))
                            return
                            ;;
                        --version)
                            COMPREPLY=($(compgen -W "latest v1.0.0" -- "$cur"))
                            return
                            ;;
                        *)
                            COMPREPLY=($(compgen -W "$install_opts -f --help -h" -- "$cur"))
                            return
                            ;;
                    esac
                    ;;
                uninstall)
                    COMPREPLY=($(compgen -W "--remove-config --remove-all-data --help -h" -- "$cur"))
                    return
                    ;;
                frontend)
                    case ${words[3]} in
                        install)
                            COMPREPLY=($(compgen -W "--auto-enable --no-auto-enable --help -h" -- "$cur"))
                            return
                            ;;
                        start)
                            case $prev in
                                --port)
                                    COMPREPLY=($(compgen -W "3000 3001 3002" -- "$cur"))
                                    return
                                    ;;
                                --host)
                                    COMPREPLY=($(compgen -W "127.0.0.1 0.0.0.0 localhost" -- "$cur"))
                                    return
                                    ;;
                                *)
                                    COMPREPLY=($(compgen -W "--port --host --help -h" -- "$cur"))
                                    return
                                    ;;
                            esac
                            ;;
                        logs)
                            case $prev in
                                --lines|-n)
                                    COMPREPLY=($(compgen -W "10 20 50 100 500" -- "$cur"))
                                    return
                                    ;;
                                *)
                                    COMPREPLY=($(compgen -W "--lines -n --follow -f --help -h" -- "$cur"))
                                    return
                                    ;;
                            esac
                            ;;
                        build)
                            COMPREPLY=($(compgen -W "--force -f --help -h" -- "$cur"))
                            return
                            ;;
                        *)
                            COMPREPLY=($(compgen -W "$frontend_commands" -- "$cur"))
                            return
                            ;;
                    esac
                    ;;
                logs)
                    case $prev in
                        --lines|-n)
                            COMPREPLY=($(compgen -W "10 20 50 100 500" -- "$cur"))
                            return
                            ;;
                        *)
                            COMPREPLY=($(compgen -W "--lines -n --help -h" -- "$cur"))
                            return
                            ;;
                    esac
                    ;;
                *)
                    COMPREPLY=($(compgen -W "$livekit_commands" -- "$cur"))
                    return
                    ;;
            esac
            ;;
            
        config)
            case ${words[2]} in
                get|set)
                    case $prev in
                        get|set)
                            # Common config keys - you could expand this list
                            COMPREPLY=($(compgen -W "VOICEMODE_TTS_PROVIDER VOICEMODE_STT_PROVIDER VOICEMODE_DEFAULT_VOICE VOICEMODE_LIVEKIT_URL VOICEMODE_LIVEKIT_API_KEY VOICEMODE_SERVICE_AUTO_ENABLE" -- "$cur"))
                            return
                            ;;
                    esac
                    ;;
                *)
                    COMPREPLY=($(compgen -W "$config_commands" -- "$cur"))
                    return
                    ;;
            esac
            ;;
            
        diag)
            COMPREPLY=($(compgen -W "$diag_commands" -- "$cur"))
            return
            ;;
            
        exchanges)
            case ${words[2]} in
                tail)
                    case $prev in
                        --format|-f)
                            COMPREPLY=($(compgen -W "$format_opts" -- "$cur"))
                            return
                            ;;
                        --date|-d)
                            # Date completion - could be enhanced
                            COMPREPLY=($(compgen -W "$(date +%Y-%m-%d) $(date -d yesterday +%Y-%m-%d)" -- "$cur"))
                            return
                            ;;
                        --transport)
                            COMPREPLY=($(compgen -W "$transport_opts" -- "$cur"))
                            return
                            ;;
                        --provider)
                            COMPREPLY=($(compgen -W "openai kokoro whisper" -- "$cur"))
                            return
                            ;;
                        *)
                            COMPREPLY=($(compgen -W "--format -f --stt --tts --full -F --no-color --date -d --transport --provider --help -h" -- "$cur"))
                            return
                            ;;
                    esac
                    ;;
                view)
                    case $prev in
                        --lines|-n)
                            COMPREPLY=($(compgen -W "10 20 50 100" -- "$cur"))
                            return
                            ;;
                        --format|-f)
                            COMPREPLY=($(compgen -W "simple pretty json" -- "$cur"))
                            return
                            ;;
                        --date|-d)
                            COMPREPLY=($(compgen -W "$(date +%Y-%m-%d) $(date -d yesterday +%Y-%m-%d)" -- "$cur"))
                            return
                            ;;
                        --conversation|-c)
                            # Could potentially list recent conversation IDs
                            return
                            ;;
                        *)
                            COMPREPLY=($(compgen -W "--lines -n --conversation -c --today --yesterday --date -d --format -f --reverse --no-color --help -h" -- "$cur"))
                            return
                            ;;
                    esac
                    ;;
                search)
                    case $prev in
                        --max-results|-n)
                            COMPREPLY=($(compgen -W "10 20 50 100" -- "$cur"))
                            return
                            ;;
                        --days|-d)
                            COMPREPLY=($(compgen -W "1 3 7 14 30" -- "$cur"))
                            return
                            ;;
                        --type)
                            COMPREPLY=($(compgen -W "$exchange_types" -- "$cur"))
                            return
                            ;;
                        --format|-f)
                            COMPREPLY=($(compgen -W "simple json" -- "$cur"))
                            return
                            ;;
                        *)
                            COMPREPLY=($(compgen -W "--max-results -n --days -d --type --regex --ignore-case -i --conversation --format -f --no-color --help -h" -- "$cur"))
                            return
                            ;;
                    esac
                    ;;
                stats)
                    case $prev in
                        --days|-d)
                            COMPREPLY=($(compgen -W "1 3 7 14 30" -- "$cur"))
                            return
                            ;;
                        *)
                            COMPREPLY=($(compgen -W "--days -d --by-hour --by-provider --by-transport --timing --conversations --errors --silence --all --help -h" -- "$cur"))
                            return
                            ;;
                    esac
                    ;;
                export)
                    case $prev in
                        --format)
                            COMPREPLY=($(compgen -W "$format_opts" -- "$cur"))
                            return
                            ;;
                        --output|-o)
                            _filedir
                            return
                            ;;
                        --date|-d)
                            COMPREPLY=($(compgen -W "$(date +%Y-%m-%d) $(date -d yesterday +%Y-%m-%d)" -- "$cur"))
                            return
                            ;;
                        --days)
                            COMPREPLY=($(compgen -W "1 3 7 14 30" -- "$cur"))
                            return
                            ;;
                        --conversation|-c)
                            # Could potentially list recent conversation IDs
                            return
                            ;;
                        *)
                            COMPREPLY=($(compgen -W "--conversation -c --date -d --days --format --include-audio --output -o --help -h" -- "$cur"))
                            return
                            ;;
                    esac
                    ;;
                *)
                    COMPREPLY=($(compgen -W "$exchanges_commands" -- "$cur"))
                    return
                    ;;
            esac
            ;;
            
        *)
            # Top-level completion
            COMPREPLY=($(compgen -W "$main_commands" -- "$cur"))
            return
            ;;
    esac
}

# Register the completion function
complete -F _voicemode_complete voicemode