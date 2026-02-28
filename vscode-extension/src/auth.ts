import * as vscode from 'vscode';

export async function requestApiKey() {
    const key = await vscode.window.showInputBox({
        prompt: 'Enter backend API key (optional)',
        ignoreFocusOut: true,
        password: true,
    });
    if (key !== undefined) {
        await vscode.workspace.getConfiguration('ai-reviewer').update('apiKey', key, vscode.ConfigurationTarget.Global);
        vscode.window.showInformationMessage('API key saved to settings.');
    }
}

export async function requestGitHubToken() {
    const token = await vscode.window.showInputBox({
        prompt: 'Enter GitHub token for OAuth actions (optional)',
        ignoreFocusOut: true,
        password: true,
    });
    if (token !== undefined) {
        await vscode.workspace.getConfiguration('ai-reviewer').update('githubToken', token, vscode.ConfigurationTarget.Global);
        vscode.window.showInformationMessage('GitHub token saved to settings.');
    }
}
