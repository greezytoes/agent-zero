const vscode = require('vscode');

function activate(context) {
    let disposable = vscode.commands.registerCommand('extension.queryAgentZero', async () => {
        const query = await vscode.window.showInputBox({ prompt: 'Enter your query for Agent Zero' });
        if (query) {
            // Here we would send the query to Agent Zero and get the response
            vscode.window.showInformationMessage('Query sent: ' + query);
        }
    });
    context.subscriptions.push(disposable);
}

function deactivate() {}

module.exports = { activate, deactivate };