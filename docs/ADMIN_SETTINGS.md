# SmartDoc Admin Settings

## Overview

The SmartDoc Admin Settings page provides a web-based interface for managing Ollama model configurations without needing to restart the application or modify configuration files directly.

## Accessing Admin Settings

1. Start the SmartDoc application
2. Navigate to `http://localhost:8080` (or your configured host/port)
3. Click on the "⚙️ Admin Settings" link in the header navigation
4. Or directly access: `http://localhost:8080/admin/settings`

## Features

### System Status
- **Ollama Server Status**: Shows whether the Ollama server is online/offline
- **Current Configuration**: Displays the active settings including:
  - Current model name
  - Base URL
  - Max tokens
  - Temperature setting

### Configuration Management
- **Ollama Base URL**: Configure the Ollama server endpoint (e.g., `http://localhost:11434`)
- **Model Name**: Select or specify the Ollama model to use (e.g., `gemma3:4b-it-q4_K_M`, `llama3.2:3b`)
- **Max Tokens**: Set the maximum number of tokens for responses (1-4096)
- **Temperature**: Control response randomness (0.0 = deterministic, 2.0 = very random)

### Testing and Validation
- **Test Connection**: Verify connectivity to the Ollama server and test the specified model
- **Load Models**: Fetch and display all available models from the Ollama server
- **Real-time Validation**: Form inputs are validated before submission

## Usage Instructions

### Changing the Model

1. Navigate to Admin Settings
2. In the "Model Name" field, enter the desired model name
3. Click "Test Connection" to verify the model is available
4. Click "Save Settings" to apply changes
5. The NLG service will be automatically reinitialized with the new model

### Testing New Settings

1. Modify the desired settings in the form
2. Click "Test Connection" to verify the configuration works
3. If successful, click "Save Settings" to apply
4. If the test fails, review the error message and adjust settings

### Loading Available Models

1. Ensure the Ollama Base URL is correct
2. Click "Load Models" to fetch available models from the server
3. Click on any model in the list to select it automatically
4. Test and save the new configuration

## Configuration Validation

The admin interface includes several validation checks:

- **URL Format**: Base URL must be a valid URL format
- **Model Name**: Cannot be empty
- **Temperature Range**: Must be between 0.0 and 2.0
- **Token Limits**: Must be between 1 and 4096
- **Server Connectivity**: Tests connection before applying changes

## Error Handling

The interface provides clear error messages for common issues:

- **Connection Errors**: When Ollama server is unreachable
- **Model Errors**: When specified model is not available
- **Validation Errors**: When input values are outside valid ranges
- **Server Errors**: When backend processing fails

## Dynamic Configuration Updates

Changes made through the admin interface:

1. **Immediate Effect**: Settings are applied immediately to the running application
2. **Session-based**: Changes persist for the current application session
3. **Service Reinitialization**: The NLG service is automatically restarted with new settings
4. **Logging**: All configuration changes are logged for audit purposes

## Recommended Models

For optimal performance with SmartDoc:

- **Small/Fast**: `gemma3:4b-it-q4_K_M` (recommended for development)
- **Balanced**: `llama3.2:3b`
- **Large/Accurate**: `llama3.2:7b` (if you have sufficient resources)

## Temperature Settings

- **0.0-0.3**: Very deterministic, consistent responses
- **0.4-0.7**: Balanced creativity and consistency (recommended)
- **0.8-1.2**: More creative and varied responses
- **1.3-2.0**: Highly creative but potentially inconsistent

## Troubleshooting

### Common Issues

1. **"Cannot connect to Ollama server"**
   - Ensure Ollama is running: `ollama serve`
   - Check the base URL is correct
   - Verify firewall settings

2. **"Model test failed"**
   - Ensure the model is installed: `ollama pull <model-name>`
   - Check model name spelling
   - Verify model exists in the available models list

3. **"Settings updated but NLG service failed to initialize"**
   - Model may be corrupted or incompatible
   - Try a different model
   - Check Ollama server logs

### Support

For additional support:
- Check the system logs at `logs/system_log.txt`
- Review Ollama server logs
- Ensure adequate system resources for the selected model
