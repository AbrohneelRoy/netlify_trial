import os
import re
import requests
import logging
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


def format_response(text):
    """
    Enhanced response formatting with:
    - Perfect code block preservation
    - Proper point formatting
    - Paragraph handling
    - Debug logging
    """
    try:
        logger.info("Starting response formatting")

        # Preserve code blocks first (with language tags)
        def preserve_code(match):
            lang = match.group(1) or 'text'
            code = match.group(2)
            logger.debug(f"Preserving code block for language: {lang}")
            return f'<div class="code-block"><span class="lang-tag">{lang}</span><pre><code>{code}</code></pre></div>'

        text = re.sub(r'```(\w*)\n([\s\S]*?)```', preserve_code, text)

        # Format points (numbered and bulleted)
        def format_points(match):
            prefix = match.group(1)
            content = match.group(2)
            if prefix.strip().endswith('.'):  # Numbered list
                return f'<div class="point"><span class="point-number">{prefix}</span><span class="point-content">{content}</span></div>'
            else:  # Bullet points
                return f'<div class="point"><span class="point-bullet">•</span><span class="point-content">{content}</span></div>'

        text = re.sub(r'^(\s*[\d•]+\.?)\s+(.+)$', format_points, text, flags=re.MULTILINE)

        # Format paragraphs
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        formatted_paragraphs = []

        for para in paragraphs:
            if not para.startswith('<div class="code-block"'):
                # Handle bold/italic in paragraphs
                para = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', para)
                para = re.sub(r'\*(.*?)\*', r'<em>\1</em>', para)
                para = f'<p>{para}</p>'
            formatted_paragraphs.append(para)

        formatted_text = ''.join(formatted_paragraphs)

        logger.info("Response formatting completed successfully")
        return f'<div class="ai-response">{formatted_text}</div>'

    except Exception as e:
        logger.error(f"Error formatting response: {str(e)}")
        return f'<div class="ai-response"><p>{text}</p></div>'


@csrf_exempt
def chat_view(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '').strip()
        logger.info(f"Received message: {user_message[:50]}...")  # Log first 50 chars

        if not user_message:
            logger.warning("Empty message received")
            return JsonResponse({'response': 'Please enter a valid message.', 'status': 'error'})

        try:
            # Prepare API request
            api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
            params = {'key': os.getenv('GEMINI_API_KEY')}
            payload = {
                "contents": [{
                    "parts": [{"text": user_message}]
                }],
                "generationConfig": {
                    "temperature": 0.7,
                    "topP": 0.9,
                    "maxOutputTokens": 2048
                }
            }

            logger.debug("Making API request...")
            response = requests.post(
                api_url,
                params=params,
                json=payload,
                timeout=25
            )
            response.raise_for_status()
            response_data = response.json()
            logger.debug("API request successful")

            try:
                raw_response = response_data['candidates'][0]['content']['parts'][0]['text']
                logger.debug(f"Raw response length: {len(raw_response)} chars")

                formatted_response = format_response(raw_response)
                logger.info("Response formatted successfully")

                return JsonResponse({
                    'response': formatted_response,
                    'raw_response': raw_response,
                    'status': 'success'
                })

            except (KeyError, IndexError) as e:
                logger.error(f"Response parsing error: {str(e)}\nFull response: {response_data}")
                return JsonResponse({
                    'response': "Sorry, I couldn't process the AI response correctly.",
                    'status': 'error'
                }, status=500)

        except requests.exceptions.Timeout:
            logger.error("Request timeout occurred")
            return JsonResponse({
                'response': "The request timed out. Please try again.",
                'status': 'error'
            }, status=504)

        except requests.exceptions.RequestException as e:
            logger.error(f"Network error: {str(e)}")
            return JsonResponse({
                'response': f"Network error: {str(e)}",
                'status': 'error'
            }, status=502)

        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            return JsonResponse({
                'response': "An unexpected error occurred. Please try again.",
                'status': 'error'
            }, status=500)

    logger.warning("Invalid request method")
    return JsonResponse({
        'error': 'Invalid request method',
        'status': 'error'
    }, status=405)


def chat_page(request):
    return render(request, 'myapp/chat.html')
