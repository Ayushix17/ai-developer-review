import axios from 'axios';
import * as vscode from 'vscode';

// Helper for calling backend API
const config = () => vscode.workspace.getConfiguration('ai-reviewer');

function getApiUrl(): string {
    return config().get<string>('apiUrl', 'http://localhost:8000');
}

function getApiKey(): string | undefined {
    return config().get<string>('apiKey');
}

async function postAnalyze(code: string): Promise<any[]> {
    const url = `${getApiUrl()}/analyze`;
    const payload = {
        diffs: [
            {
                file_name: 'selection',
                file_path: 'selection',
                language: 'python',
                new_code: code,
            },
        ],
        repository_context: '',
        include_ast_analysis: config().get<boolean>('enableAST', true),
        include_rag: config().get<boolean>('enableRAG', true),
        use_expensive_model: false,
    };

    const headers: any = {};
    const key = getApiKey();
    if (key) headers['Authorization'] = `Bearer ${key}`;

    const resp = await axios.post(url, payload, { headers, timeout: 30000 });
    return resp.data;
}

export async function analyzeCode(code: string): Promise<any[]> {
    try {
        const data = await postAnalyze(code);
        return data;
    } catch (err) {
        throw err;
    }
}

export async function improveCode(code: string): Promise<any[]> {
    // for now treat as analyze (could send prompt type)
    return analyzeCode(code);
}

export async function explainCode(code: string): Promise<string> {
    try {
        // simply ask backend for a review and return summary
        const data = await postAnalyze(code);
        if (Array.isArray(data) && data.length && data[0].summary) {
            return data[0].summary;
        }
        return 'No explanation available';
    } catch (err) {
        throw err;
    }
}
