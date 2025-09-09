// Cloudflare Worker for voicemode.sh
// Serves install script to CLI tools, website to browsers
// Deploy with: wrangler publish or via Cloudflare dashboard

// The install script URL - we'll fetch from GitHub
const INSTALL_SCRIPT_URL = 'https://raw.githubusercontent.com/mbailey/voicemode/main/docs/web/install.sh';

// Cache install script for 5 minutes to reduce GitHub requests
const CACHE_TTL = 300;

// Simple landing page for browsers
const HTML_PAGE = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VoiceMode - Voice Conversations for AI Coding Assistants</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            padding: 60px;
            max-width: 800px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        h1 {
            font-size: 3em;
            margin-bottom: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .tagline {
            font-size: 1.5em;
            color: #666;
            margin-bottom: 40px;
        }
        .install-box {
            background: #1e1e1e;
            color: #fff;
            padding: 20px;
            border-radius: 10px;
            margin: 30px 0;
            font-family: 'Courier New', monospace;
            position: relative;
        }
        .install-cmd {
            color: #4fc3f7;
            user-select: all;
            font-size: 1.1em;
        }
        .copy-btn {
            position: absolute;
            top: 10px;
            right: 10px;
            background: #667eea;
            color: white;
            border: none;
            padding: 5px 15px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 0.9em;
        }
        .copy-btn:hover {
            background: #764ba2;
        }
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 30px;
            margin: 40px 0;
        }
        .feature {
            text-align: center;
        }
        .feature-icon {
            font-size: 3em;
            margin-bottom: 15px;
        }
        .links {
            margin-top: 40px;
            display: flex;
            gap: 20px;
            justify-content: center;
            flex-wrap: wrap;
        }
        .btn {
            display: inline-block;
            padding: 12px 30px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 30px;
            transition: transform 0.2s;
        }
        .btn:hover {
            transform: translateY(-2px);
            background: #764ba2;
        }
        .btn-secondary {
            background: transparent;
            border: 2px solid #667eea;
            color: #667eea;
        }
        .btn-secondary:hover {
            background: #667eea;
            color: white;
        }
        @media (max-width: 600px) {
            .container {
                padding: 30px;
            }
            h1 {
                font-size: 2em;
            }
            .tagline {
                font-size: 1.2em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎙️ VoiceMode</h1>
        <p class="tagline">Voice conversations for AI coding assistants</p>
        
        <div class="install-box">
            <button class="copy-btn" onclick="copyInstall()">Copy</button>
            <code class="install-cmd">curl -sSf https://voicemode.sh | sh</code>
        </div>
        
        <div class="features">
            <div class="feature">
                <div class="feature-icon">🤖</div>
                <h3>Claude Code Integration</h3>
                <p>Seamless MCP server for voice tools</p>
            </div>
            <div class="feature">
                <div class="feature-icon">🔒</div>
                <h3>Privacy First</h3>
                <p>Run locally or use cloud services</p>
            </div>
            <div class="feature">
                <div class="feature-icon">🚀</div>
                <h3>Easy Setup</h3>
                <p>One command installs everything</p>
            </div>
        </div>
        
        <div class="links">
            <a href="https://github.com/mbailey/voicemode" class="btn">GitHub</a>
            <a href="https://github.com/mbailey/voicemode#readme" class="btn btn-secondary">Documentation</a>
        </div>
    </div>
    
    <script>
        function copyInstall() {
            const cmd = 'curl -sSf https://voicemode.sh | sh';
            navigator.clipboard.writeText(cmd).then(() => {
                const btn = document.querySelector('.copy-btn');
                btn.textContent = 'Copied!';
                setTimeout(() => {
                    btn.textContent = 'Copy';
                }, 2000);
            });
        }
    </script>
</body>
</html>`;

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const userAgent = request.headers.get('User-Agent') || '';
    
    // Detect CLI tools (curl, wget, etc.)
    const isCLI = /curl|wget|fetch|httpie|powershell|invoke-webrequest/i.test(userAgent);
    
    // Analytics tracking (optional)
    if (url.pathname === '/analytics') {
      return handleAnalytics(request, env);
    }
    
    // Force install script at /install or /install.sh
    if (url.pathname === '/install' || url.pathname === '/install.sh') {
      return await serveInstallScript(env);
    }
    
    // Root path: detect user agent
    if (url.pathname === '/' || url.pathname === '') {
      if (isCLI) {
        // CLI tools get the installer script
        return await serveInstallScript(env);
      } else {
        // Browsers get the website
        return new Response(HTML_PAGE, {
          headers: {
            'Content-Type': 'text/html; charset=utf-8',
            'Cache-Control': 'public, max-age=3600',
            'X-Content-Type-Options': 'nosniff',
          }
        });
      }
    }
    
    // 404 for everything else
    return new Response('Not Found', { 
      status: 404,
      headers: {
        'Content-Type': 'text/plain',
      }
    });
  }
};

async function serveInstallScript(env) {
  // Try to get from cache first
  const cache = caches.default;
  const cacheKey = new Request('https://voicemode.sh/install-script-cache');
  
  let response = await cache.match(cacheKey);
  
  if (!response) {
    // Fetch from GitHub
    try {
      const scriptResponse = await fetch(INSTALL_SCRIPT_URL, {
        headers: {
          'User-Agent': 'VoiceMode-Worker/1.0',
        }
      });
      
      if (!scriptResponse.ok) {
        throw new Error(`GitHub returned ${scriptResponse.status}`);
      }
      
      const script = await scriptResponse.text();
      
      // Create response with proper headers
      response = new Response(script, {
        headers: {
          'Content-Type': 'text/x-shellscript; charset=utf-8',
          'Cache-Control': `public, max-age=${CACHE_TTL}`,
          'X-Content-Type-Options': 'nosniff',
          'X-Install-Source': 'github',
        }
      });
      
      // Cache it
      ctx.waitUntil(cache.put(cacheKey, response.clone()));
      
    } catch (error) {
      // Fallback to embedded minimal script
      const fallbackScript = `#!/bin/sh
# VoiceMode installer is temporarily unavailable
# Please try again later or install from GitHub:
# 
# git clone https://github.com/mbailey/voicemode
# cd voicemode
# ./install.sh

echo "VoiceMode installer is temporarily unavailable."
echo "Please visit: https://github.com/mbailey/voicemode"
exit 1
`;
      
      response = new Response(fallbackScript, {
        headers: {
          'Content-Type': 'text/x-shellscript; charset=utf-8',
          'Cache-Control': 'no-cache',
          'X-Install-Source': 'fallback',
        }
      });
    }
  }
  
  return response;
}

async function handleAnalytics(request, env) {
  // Simple analytics endpoint
  const data = {
    timestamp: new Date().toISOString(),
    country: request.headers.get('CF-IPCountry') || 'unknown',
    userAgent: request.headers.get('User-Agent') || 'unknown',
  };
  
  // Could store in Workers KV, Durable Objects, or external service
  // For now, just return success
  return new Response(JSON.stringify({ status: 'ok', data }), {
    headers: {
      'Content-Type': 'application/json',
    }
  });
}