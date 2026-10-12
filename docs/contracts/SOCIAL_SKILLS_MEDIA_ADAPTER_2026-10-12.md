# Adopción selectiva de Social Media Skills: NINFA Media Handoff

Fecha: 2026-10-12 | Estado: SPEC/ADAPTER CANDIDATE, NO RELEASE CERTIFIED

## Evidencia y procedencia
Original: https://github.com/charlie947/social-media-skills; fork: https://github.com/Em3rc0d/social-media-skills; commit observado: 8cefb5b6d03757885faa6918bd8bfaef202a83db (versión 1.1.0). Copyright 2026 Charlie Hills / MIT. Se extraen abstracciones, no recursos, fotografías, textos completos ni dependencias del autor. Ninguna skill externa aporta pruebas de publicación ni acceso a sus cuentas.

## Qué se incorpora
- De reels-scripting: estructura de referencia -> mecanismo del hook -> guion ORIGINAL -> caption alineado -> revisión. No copiar palabras, experiencia ni una secuencia visual completa de terceros. Una referencia no es outlier sin línea base comparable del mismo creador.
- De graphic-designer y gemini-carousel: distinguir BRIEF / PROMPT_READY / SOURCE_RENDERABLE / RENDERED_UNREVIEWED / HUMAN_VISUALLY_REVIEWED. Inspeccionar píxeles reales en resolución original y tamaño de feed, slide por slide.
- De youtube-thumbnail: primero cerrar una promesa verificable de título/miniatura; no inventar resultados del experimento; texto grande y safe areas adecuadas al canal.
- De analytics-dashboard: vincular hipótesis por formato con CTR, primeros 30 segundos, retención, completado y siguiente vídeo. Sin benchmarks genéricos ni predicción falsa de viralidad.
- De voice-builder: usar únicamente Voice/Brand versionados de NINFA, nunca muestras por defecto ni reglas británicas externas. La identidad Does It Automate? es inglesa; las cuentas en es-PE conservan su propia autoridad.
- De content-matrix: reutilizar mecanismos narrativos, NO repetir incidentes, hook, escena, gag o lección. Un vídeo fuente puede dar 2-3 shorts sólo si cada derivado tiene aprendizaje materialmente distinto.

## Contrato de entrada: Consumer, no propietario
El opt-in candidato se define en Em3rc0d/content-seller: mk1/integration/EDITORIAL_TO_MEDIA_V1.schema.json y su preflight local. Esta ruta no forma parte de prodAgentic ContentPackageV1 ni de los esquemas de escenas/shorts de NINFA.

Campos necesarios del brief recibido:
- content_id, profile_id, platform, locale, objective, topic_id, angle_id, hook_family, hook, caption, cta;
- media.format, media.visual_job, media.aspect_ratio, media.script_or_storyboard_ref, media.render_status;
- evidence.claim_review + evidence_refs + review_ref;
- novelty.status + ledger_ref + review_ref + las ocho dimensiones;
- editorial_gate; release.publish_authority = NONE; scheduled_at = null; provider_receipt = null.

Proceso:
1. Verificar explícitamente identidad y canal. NINFA no hereda assets de Content Seller ni traslada una voz en inglés a un perfil español. Si no corresponde el perfil y canal autorizados, BLOCKED.
2. Ejecutar el preflight del productor/editorial (Content Seller). Un STRUCTURALLY_READY_FOR_MEDIA es autorización de trabajo editorial, nunca prueba semántica o permiso de publicación. Comprobar que las referencias reales existan en su ledger antes de utilizar claims.
3. Resolver script -> storyboard -> shotlist/scene manifest, con sentido audiovisual: cada movimiento explica input, transformación, contradicción o resultado. No forzar pantalla estática de diapositivas.
4. Resolver el contrato NINFA propio para cada canal. shorts-motion-v1.schema.json hoy sólo acepta inglés y no certifica formatos TikTok es-PE; NO relajar su const locale ni convertir sus fixtures en producción. Un nuevo canal requiere su propio contrato, safe-zones y tests antes de render.
5. Para Does It Automate? se conserva Brand Identity V1 > Channel Thesis > Shorts Motion Contract > scene template. El vídeo de ejemplo sintetizado nunca prueba cliente o proveedor real.
6. Render local y assets auténticos, con $0 de APIs de pago por defecto. La voz grabada de propietario permanece fuera de GitHub; no consumir GitHub Actions para medios. No se exige nueva instalación de Apify/Gemini ni servicios externos.
7. Validar audio escuchado, subtítulos frase por frase, material probatorio, tipografía, ratio 1080×1920, overlays de la plataforma, derechos, marca y cada visual en tamaño feed. Prompt ≠ PNG ≠ MP4 revisado.
8. Entregar package con asset hashes, QA real + pendientes, versión de brief, links de fuentes, captions exactos; pasar a revisión humana. release-gates.json/PUBLISHING authority no cambian aquí.
9. Publicación/programación pertenecen al owner autorizado/prodAgentic. Sin provider receipt, no afirmar Scheduled/Published; sin reconciliación, estado UNKNOWN/RECONCILIATION_REQUIRED en lugar de blind retry.

## Pruebas adversariales de aceptación (manuales, para futura automatización)
- E1: input con novelty=PENDING -> BLOCKED antes de render final.
- E2: evidencia no disponible -> no convertir el resultado esperado en titular fáctico.
- E3: idioma es-PE para contrato actual Does It Automate? inglés -> BLOCKED, no traducir en silencio.
- E4: prompt de miniatura sin PNG real -> PROMPT_READY, no VISUALLY_REVIEWED.
- E5: mismo incidente repartido en 3 clips con la misma lección -> rechazar derivaciones 2 y 3.
- E6: QA técnica PASS pero safe-area telefónica PENDING -> release BLOCKED.
- E7: aprobación humana ausente y render válido -> delivery para revisión; jamás Scheduled/Published.
- E8: el logo no está provisto y validado -> omitirlo, no generar uno ficticio.

## Estado operativo
No se han modificado scene engines, voz, contrato congelado, fixtures existentes ni pipeline de distribución. La adopción está documentada como handoff no autoritativo y solo puede convertirse en integración ejecutable tras E1-E8 y un owner UAT independiente. La prueba de contrato preexistente no suple la prueba de visuales ni rendimiento de vídeo.

## QA de posts premium — 2026-10-12

[Resumen de aceptación estética, uncanny valley, bytes finales y estados de publicación](PREMIUM_POST_MEDIA_QA_2026-10-12.md). Es extracción de conocimiento para medios, no un bridge ejecutable con PlacaClara ni una modificación del contrato audiovisual en inglés.
