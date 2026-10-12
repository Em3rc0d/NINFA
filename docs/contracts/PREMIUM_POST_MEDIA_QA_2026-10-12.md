# Premium social-media QA — material estático y audiovisuales
Fecha: 2026-10-12 | Nivel: KNOWLEDGE/TEST ADVICE. No modifica runtime, schemas de Shorts o brand identities.

## Casos observados
- Content Seller: post educativo SQLite exacto pero con composición plana; rechazado por el propietario.
- PlacaClara: pieza comercial premium aceptada como dirección visual, con escena humana más natural tras un ajuste contra uncanny valley. Referencia: [plate PR #8](https://github.com/Em3rc0d/plate/pull/8), `PC-20261012-COVERAGE-DATE-001`. El PNG aprobado como dirección no equivale a PNG pixel-perfect final ni a publicación.
- La normalización de 941×1672 a 1080×1920 mantiene contenido, **no** mueve automáticamente CTA/logos fuera de overlays.

## Gates recomendados para futuros jobs soportados (nunca un PASS sintético)
1. BRAND_INPUT: perfil, marca/idioma y master de logo proporcionados por propietario; una imagen similar a la marca no acredita fidelidad.
2. VISUAL_JOB: protagonista que explique el conflicto real, composición profunda y sin sobreuso de tarjetas; el estilo no debe clonarse entre temas.
3. HUMAN_REALISM: proporciones, manos, smartphone y expresiones naturales; corregir uncanny valley sin sustituir un humano ficticio por testimonio/cliente real.
4. TEXT_PRECISION: palabras, precio, etiquetas de UI/código y acentos cotejados línea por línea; renderizado tipográfico determinista preferido cuando se necesite exactitud.
5. REAL_OUTPUT: inspect PNG/MP4 con dimensiones reales y preview móvil; safe zones del **canal concreto**, no de otra marca ni de otra fecha.
6. LICENSE/EVIDENCE: derechos, procedencia, datos reales, ausencia de falsas pantallas/resultados, ilustración claramente identificada.
7. OWNER_CREATIVE_DIRECTION ≠ EXACT_ARTIFACT_SIGNOFF ≠ PLATFORM_QA ≠ PROVIDER_RECEIPT: gates separados.
8. PUBLISHER_BOUNDARY: preparar material no implica autorizar programación/publicación. Sin hash+receipt no marcar SCHEDULED/PUBLISHED.

## Contrato de compatibilidad
NINFA hoy no integra el `placaclara-social-package/v1` de `plate`, y sus Shorts ingleses siguen regidos por su contrato propio. Esta nota NO crea un adapter, no acepta `es-PE` en el schema congelado ni da acceso a la cuenta PlacaClara. Si un futuro trabajo multimedia lo necesita, abrir MK de compatibilidad con UAT y owner de canal, sin contaminar Does It Automate?.

## Evidencia faltante
- Prueba de que estos criterios realmente elevan retención, conversión o tiempo.
- Validación visual de TikTok Studio/Instagram para el binario elegido.
- Un parser/bridge operativo NINFA→PlacaClara, inexistente.
