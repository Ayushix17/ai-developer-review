"""
VS Code Extension - Main entry point
Phase 7: Scaffold extension, authenticate, send code to backend, show suggestions
"""

import * as vscode from 'vscode';

export async function activate(context: vscode.ExtensionContext) {
    console.log('AI Code Reviewer extension activated');

    // Register commands
    context.subscriptions.push(
        vscode.commands.registerCommand('ai-reviewer.analyze', async () => {
            const editor = vscode.window.activeTextEditor;
            if (!editor) return;

            const selectedText = editor.document.getText(editor.selection);
            if (!selectedText) {
                vscode.window.showWarningMessage('Please select some code to analyze');
                return;
            }

            try {
                const suggestions = await analyzeCode(selectedText);
                showSuggestions(suggestions);
            } catch (error) {
                vscode.window.showErrorMessage(`Analysis failed: ${error}`);
            }
        }),

        vscode.commands.registerCommand('ai-reviewer.improve', async () => {
            const editor = vscode.window.activeTextEditor;
            if (!editor) return;

            const selectedText = editor.document.getText(editor.selection);
            if (!selectedText) {
                vscode.window.showWarningMessage('Please select some code to improve');
                return;
            }

            try {
                const suggestions = await improveCode(selectedText);
                showSuggestions(suggestions);
            } catch (error) {
                vscode.window.showErrorMessage(`Improvement suggestion failed: ${error}`);
            }
        }),

        vscode.commands.registerCommand('ai-reviewer.explain', async () => {
            const editor = vscode.window.activeTextEditor;
            if (!editor) return;

            const selectedText = editor.document.getText(editor.selection);
            if (!selectedText) {
                vscode.window.showWarningMessage('Please select some code to explain');
                return;
            }

            try {
                const explanation = await explainCode(selectedText);
                vscode.window.showInformationMessage(explanation);
            } catch (error) {
                vscode.window.showErrorMessage(`Explanation failed: ${error}`);
            }
        }),

        vscode.commands.registerCommand('ai-reviewer.settings', async () => {
            vscode.commands.executeCommand('workbench.action.openSettings', 'ai-reviewer');
        })
    );

    // Status bar item
    const statusBar = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    statusBar.text = '$(sparkle) AI Reviewer Ready';
    statusBar.show();
    context.subscriptions.push(statusBar);
}

export function deactivate() {
    console.log('AI Code Reviewer extension deactivated');
}

async function analyzeCode(code: string) {
    // Implementation will connect to backend
    return [];
}

async function improveCode(code: string) {
    // Implementation will connect to backend
    return [];
}

async function explainCode(code: string): Promise<string> {
    // Implementation will connect to backend
    return '';
}

function showSuggestions(suggestions: any[]) {
    // Show suggestions in UI
}
