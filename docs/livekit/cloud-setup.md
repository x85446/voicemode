# LiveKit Cloud Setup Guide for Voice MCP

This guide will get you talking to Claude through LiveKit Cloud in about 15 minutes.

## Prerequisites

- [ ] Voice MCP installed and working locally
- [ ] OpenAI API key configured
- [ ] A web browser
- [ ] (Optional) iPhone with TestFlight for voice-assistant-swift

## Step 1: Create a LiveKit Cloud Account

1. Go to [LiveKit Cloud](https://cloud.livekit.io)
2. Click **"Sign Up"** or **"Get Started Free"**
3. Create your account (GitHub login works great)
4. You'll get free monthly credits - more than enough for personal use

## Step 2: Create Your First Project

1. Once logged in, click **"Create Project"**
2. Name it something like `voice-mcp-sandbox`
3. Select the closest region to you
4. Click **"Create"**

## Step 3: Get Your Connection Details

You'll need three things from LiveKit Cloud:

1. **Project URL**: Found at the top of your project dashboard
   - Looks like: `wss://your-project-name.livekit.cloud`
   
2. **API Key**: In project settings → API Keys
   - Click **"Create Key"**
   - Give it a name like `voice-mcp-key`
   - Copy the **API Key** (starts with `API`)
   
3. **API Secret**: Shown once when you create the key
   - Copy it immediately (you won't see it again!)
   - If you lose it, just create a new key

## Step 4: Configure Voice MCP

Add these to your environment:

```bash
# Your existing OpenAI key
export OPENAI_API_KEY="your-openai-key"

# New LiveKit configuration
export LIVEKIT_URL="wss://your-project-name.livekit.cloud"
export LIVEKIT_API_KEY="your-api-key-from-step-3"
export LIVEKIT_API_SECRET="your-api-secret-from-step-3"
```

### For Claude Code:
```bash
claude mcp restart voice-mcp
```

### For Claude Desktop:
Update your config file to include the LiveKit environment variables, then restart Claude Desktop.

## Step 5: Test the Connection

In Claude, try:
```
"Check LiveKit room status"
```

You should see a response about LiveKit rooms. If you get an error, double-check your credentials.

## Step 6: Connect from a Web Frontend

### Option A: LiveKit Playground (Quickest)

1. Go to your LiveKit Cloud dashboard
2. Find the **"Playground"** or **"Demo"** section
3. Click **"Voice Assistant"** or similar demo
4. It should connect to your project automatically

### Option B: Voice Assist Frontend

1. Clone the LiveKit examples:
   ```bash
   git clone https://github.com/livekit-examples/voice-assistant-frontend.git
   cd voice-assistant-frontend
   ```

2. Create a `.env.local` file:
   ```
   LIVEKIT_URL=wss://your-project-name.livekit.cloud
   LIVEKIT_API_KEY=your-api-key
   LIVEKIT_API_SECRET=your-api-secret
   ```

3. Install and run:
   ```bash
   npm install
   npm run dev
   ```

4. Open http://localhost:3000 in your browser

### Option C: LiveKit Meet (Simple Testing)

1. Go to [meet.livekit.io](https://meet.livekit.io)
2. Click "Custom" tab
3. Enter your LiveKit URL and a token (generate one from CLI or dashboard)

## Step 7: Start Talking!

1. In Claude, say:
   ```
   "Let's have a voice conversation through LiveKit"
   ```

2. Claude will connect to a LiveKit room
3. Open your web frontend and join the same room
4. Start talking - you should hear Claude respond!

## Step 8: iPhone Setup (voice-assistant-swift)

1. Install TestFlight on your iPhone
2. Get the voice-assistant-swift TestFlight link (check LiveKit's GitHub)
3. In the app settings, enter:
   - Server URL: Your LiveKit URL
   - API Key: Your API key
   - API Secret: Your API secret
4. Join a room and start talking!

## Troubleshooting

### "Connection failed" in Claude
- Check your LIVEKIT_URL starts with `wss://` (not `https://`)
- Verify API credentials are correct
- Try `claude mcp restart voice-mcp`

### No audio in web frontend
- Check browser permissions for microphone
- Ensure you're using HTTPS (or localhost)
- Try a different browser

### Can't hear Claude's responses
- Check speaker/headphone connection
- Verify OpenAI API key is working
- Look for errors in Claude's responses

## What's Next?

Now that you have LiveKit Cloud working:

1. **Mobile Access**: Install voice-assistant apps on your devices
2. **Custom Frontend**: Build your own web interface
3. **Advanced Features**: Explore recording, transcription, and more

## Useful Commands

Test LiveKit connection:
```
"Check LiveKit room status"
```

Start a conversation:
```
"Let's have a voice conversation through LiveKit"
```

Force LiveKit transport:
```
"Talk to me using LiveKit transport"
```

## Resources

- [LiveKit Cloud Dashboard](https://cloud.livekit.io)
- [LiveKit Documentation](https://docs.livekit.io)
- [Voice Assistant Examples](https://github.com/livekit-examples)
- [Voice MCP Issues](https://github.com/mbailey/voice-mcp/issues)