css = '''
<style>
/* Main chat container */
.chat-container {
    display: flex;
    flex-direction: column;
    height: calc(100vh - 200px);
    overflow-y: auto;
    padding: 2rem;
}

/* Message styling */
.chat-message {
    display: flex;
    align-items: flex-start;
    padding: 1.5rem;
    margin-bottom: 1rem;
    max-width: 80%;
}

.chat-message.user {
    margin-left: auto;
    background-color: #2b313e;
    border-radius: 1rem 0.25rem 1rem 1rem;
}

.chat-message.bot {
    margin-right: auto;
    background-color: #475063;
    border-radius: 0.25rem 1rem 1rem 1rem;
}

/* Avatar styling */
.chat-message .avatar {
    flex: 0 0 40px;  /* Don't allow avatar to shrink or grow */
    width: 40px;
    height: 40px;
    margin-right: 1rem;
}

.chat-message .avatar img {
    width: 40px;
    height: 40px;
    border-radius: 0.5rem;
    object-fit: cover;
}

/* Message content */
.chat-message .message {
    flex: 1;  /* Allow message to take remaining space */
    color: #fff;
    font-size: 1rem;
    line-height: 1.5;
    word-wrap: break-word;  /* Ensure long words don't overflow */
    min-width: 0;  /* Allow flex item to shrink below content size */
}

/* Input container */
.input-container {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: #262730;
    padding: 1.5rem;
    border-top: 1px solid #4a4a4a;
}

/* Custom scrollbar */
.chat-container::-webkit-scrollbar {
    width: 6px;
}

.chat-container::-webkit-scrollbar-track {
    background: transparent;
}

.chat-container::-webkit-scrollbar-thumb {
    background: #4a4a4a;
    border-radius: 3px;
}

.chat-container::-webkit-scrollbar-thumb:hover {
    background: #555;
}
</style>
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.ibb.co/cN0nmSj/Screenshot-2023-05-28-at-02-37-21.png" alt="Bot Avatar">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://i.ibb.co/rdZC7LZ/Photo-logo-1.png" alt="User Avatar">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''