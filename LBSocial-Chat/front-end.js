import { handleUserMessage } from 'backend/chatbot';

$w.onReady(function () {
    let messages = []; // Store conversation log

    const logMessage = (role, content) => {
        messages.push({ role, content });
    };

    // Handle user messages from Wix Chatbox
    $w('#wixChat').onMessageSent(async (message) => {
        const channelId = message.channelId;
        const userMessage = message.payload.text;

        logMessage("user", userMessage);

        // Send message to backend chatbot
        await handleUserMessage(userMessage, channelId);
    });

    // Ensure bot responses are not logged as user messages
    $w('#wixChat').onMessageReceived((message) => {
        if (message.direction === "BusinessToVisitor") {
            logMessage("bot", message.payload.text);
        }
    });
});
