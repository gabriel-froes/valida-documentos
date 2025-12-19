import json
from typing import Any, Dict, List

import httpx

from app.core.config import settings
from app.core.exceptions import (
    LLMClientError,
    LLMJSONParseError,
    LLMResponseError,
    LLMTimeoutError,
)
from app.core.logging import get_logger

logger = get_logger(__name__)


async def call_llm(messages: List[Dict[str, str]]) -> Dict[str, Any]:
    headers: Dict[str, str] = {
        'Authorization': f'Bearer {settings.openrouter_api_key}',
        'Content-Type': 'application/json',
    }

    payload: Dict[str, Any] = {
        'model': settings.openrouter_model,
        'messages': messages,
        'temperature': settings.openrouter_temperature,
        'response_format': {'type': 'json_object'},
    }

    async with httpx.AsyncClient(timeout=settings.llm_timeout_seconds) as client:
        try:
            response = await client.post(
                settings.openrouter_base_url,
                json=payload,
                headers=headers,
            )
        except httpx.TimeoutException as exc:
            logger.error(
                "LLM timeout error",
                extra={
                    "data": {
                        "error": str(exc),
                        "model": settings.openrouter_model,
                        "timeout_seconds": settings.llm_timeout_seconds,
                    },
                },
            )
            raise LLMTimeoutError(
                "O serviço de processamento de documentos demorou muito para responder. Tente novamente."
            ) from exc
        except httpx.HTTPError as exc:
            logger.error(
                "LLM HTTP error",
                extra={"data": {"error": str(exc), "model": settings.openrouter_model}},
            )
            raise LLMClientError(
                "Erro ao comunicar com o serviço de processamento. Tente novamente mais tarde."
            ) from exc

        if response.status_code >= 400:
            error_detail = response.text[:500] if response.text else "No error details"
            logger.error(
                "LLM API error",
                extra={
                    "data": {
                        "status_code": response.status_code,
                        "model": settings.openrouter_model,
                        "error_preview": error_detail,
                    },
                },
            )
            raise LLMClientError(
                "Erro no serviço de processamento de documentos. Tente novamente mais tarde."
            )
        
        try:
            return response.json()
        except json.JSONDecodeError as exc:
            logger.error(
                "LLM response JSON decode error",
                extra={
                    "data": {
                        "model": settings.openrouter_model,
                        "response_preview": response.text[:200] if response.text else None,
                    },
                },
            )
            raise LLMClientError(
                "Resposta inválida do serviço de processamento. Tente novamente."
            ) from exc


def parse_llm_json_response(response: Dict[str, Any]) -> Dict[str, Any]:
    try:
        if "choices" not in response or not response["choices"]:
            raise LLMResponseError(
                "Resposta inválida do serviço de processamento. Tente novamente."
            )
        
        if "message" not in response["choices"][0]:
            raise LLMResponseError(
                "Resposta inválida do serviço de processamento. Tente novamente."
            )
        
        if "content" not in response["choices"][0]["message"]:
            raise LLMResponseError(
                "Resposta inválida do serviço de processamento. Tente novamente."
            )
        
        content = response["choices"][0]["message"]["content"]
        
        if not content or not content.strip():
            raise LLMResponseError(
                "Resposta vazia do serviço de processamento. Tente novamente."
            )
        
        return json.loads(content)
    except json.JSONDecodeError as exc:
        logger.error(
            "LLM content JSON parse error",
            extra={
                "data": {
                    "content_preview": content[:200] if isinstance(content, str) else str(content)[:200],
                },
            },
        )
        raise LLMJSONParseError(
            "Não foi possível processar a resposta do serviço. Tente novamente."
        ) from exc
    except KeyError as exc:
        logger.error(
            "LLM response structure error",
            extra={"data": {"missing_key": str(exc), "response_keys": list(response.keys())}},
        )
        raise LLMResponseError(
            "Estrutura de resposta inválida do serviço. Tente novamente."
        ) from exc


async def call_llm_and_parse(content: str) -> Dict[str, Any]:
    messages = [{"role": "user", "content": content}]
    response = await call_llm(messages)
    return parse_llm_json_response(response)