#!/bin/bash

# sysopctl version
VERSION="v0.1.0"

# Function to show help
function show_help() {
    echo "sysopctl - System Operation Control"
    echo "Usage: sysopctl [option] [arguments]"
    echo ""
    echo "Options:"
    echo "  --help           Show this help message"
    echo "  --version        Show the command version"
    echo ""
    echo "Commands:"
    echo "  service list            List all running services"
    echo "  service start <name>    Start a service"
    echo "  service stop <name>     Stop a service"
    echo "  system load             Show system load averages"
    echo "  disk usage              Show disk usage"
}

# Function to show version
function show_version() {
    echo "sysopctl version $VERSION"
}

# Function to list running services
function list_services() {
    systemctl list-units --type=service
}

# Function to start a service
function start_service() {
    systemctl start "$1"
    echo "Service $1 started."
}

# Function to stop a service
function stop_service() {
    systemctl stop "$1"
    echo "Service $1 stopped."
}

# Function to show system load
function show_system_load() {
    uptime
}

# Function to show disk usage
function show_disk_usage() {
    df -h
}

# Parse the command-line arguments
case "$1" in
    --help)
        show_help
        ;;
    --version)
        show_version
        ;;
    service)
        case "$2" in
            list)
                list_services
                ;;
            start)
                start_service "$3"
                ;;
            stop)
                stop_service "$3"
                ;;
            *)
                echo "Unknown service command."
                show_help
                ;;
        esac
        ;;
    system)
        case "$2" in
            load)
                show_system_load
                ;;
            *)
                echo "Unknown system command."
                show_help
                ;;
        esac
        ;;
    disk)
        case "$2" in
            usage)
                show_disk_usage
                ;;
            *)
                echo "Unknown disk command."
                show_help
                ;;
        esac
        ;;
    *)
        echo "Unknown option or command."
        show_help
        ;;
esac
