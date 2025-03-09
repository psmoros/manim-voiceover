"""
CLI entrypoint for manim-voiceover
"""

import inspect
import os
import sys
from pathlib import Path

from manim.cli.render.commands import main_command, render

from manim_voiceover.cli.config import add_voiceover_args

# Hook into the Manim CLI by monkey patching the main command
original_render_command = render.command

def patched_render_command(function):
    # Call the original decorated function
    cmd = original_render_command(function)
    
    # Get the 'params' attribute from the decorated function
    params = getattr(cmd, 'params', [])
    
    # Add our custom arguments to the command line
    def param_callback(ctx, param, value):
        # Store the use_cloud_whisper value in the context object
        ctx.ensure_object(dict)
        ctx.obj['use_cloud_whisper'] = value
        return value
    
    # Add our parameter to the command
    from click import option
    cmd = option('--use-cloud-whisper', 
                 is_flag=True, 
                 help='Use OpenAI cloud API for Whisper instead of local model',
                 callback=param_callback)(cmd)
    
    return cmd

# Apply our monkey patch
render.command = patched_render_command

# Also hook into the argparse version of the CLI
original_main = main_command

def patched_main():
    """Entry point for renderer."""
    # Find the render subcommand in the argument parser
    import argparse
    
    # Create a dummy parser just to intercept the args
    dummy_parser = argparse.ArgumentParser(add_help=False)
    dummy_parser.add_argument("--use-cloud-whisper", action="store_true")
    
    # Parse known args to get our flags
    args, unknown = dummy_parser.parse_known_args()
    
    # Set the global config value
    from manim.config import config
    if hasattr(args, 'use_cloud_whisper') and args.use_cloud_whisper:
        config.use_cloud_whisper = True
    
    # Call the original main command
    return original_main()

# Apply our second monkey patch
main_command = patched_main 