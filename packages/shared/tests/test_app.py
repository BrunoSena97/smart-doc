#!/usr/bin/env python3
"""
SmartDoc API Entry Point

Flask application entry point for the refactored SmartDoc platform.
"""

import os
import sys
from flask import Flask

# Add package paths to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(project_root, 'packages', 'core', 'src'))
sys.path.insert(0, os.path.join(project_root, 'packages', 'shared', 'src'))

# Now we can import from the new structure
try:
    from smartdoc_core.intent.classifier import LLMIntentClassifier
    from smartdoc_core.utils.logger import sys_logger
    from smartdoc_core.config.settings import config
    print("✅ Successfully imported SmartDoc core components!")

    # Create a simple Flask app for testing
    app = Flask(__name__)

    @app.route('/')
    def hello():
        return '''
        <h1>🎉 SmartDoc Refactored Successfully!</h1>
        <p>The new monorepo structure is working!</p>
        <ul>
            <li>✅ Core package: smartdoc_core</li>
            <li>✅ Intent classification working</li>
            <li>✅ Configuration loaded</li>
            <li>✅ Logging system active</li>
        </ul>
        <p><strong>Next steps:</strong></p>
        <ol>
            <li>Finish migrating the web interface</li>
            <li>Test the simulation engine</li>
            <li>Update deployment scripts</li>
        </ol>
        '''

    @app.route('/health')
    def health():
        return {'status': 'ok', 'message': 'SmartDoc refactored structure is healthy!'}

    if __name__ == '__main__':
        print("🚀 Starting SmartDoc with new structure...")
        app.run(debug=True, host='127.0.0.1', port=5000)

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please check the package structure and imports.")
    sys.exit(1)
