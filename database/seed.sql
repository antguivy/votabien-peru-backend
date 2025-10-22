-- =====================================================
-- SEED DATA - Vota Bien Peru
-- Este script carga datos de ejemplo para desarrollo
-- =====================================================

-- Nota: Este script solo se ejecutará si las tablas están vacías
-- Los IDs son CUID generados manualmente para este ejemplo

-- =====================================================
-- 1. PARTIDOS POLÍTICOS
-- =====================================================

INSERT INTO partidopolitico (
    id, nombre, sigla, logo_url, color_hex, activo,
    fundador, fecha_fundacion, descripcion, ideologia,
    sede_nacional, telefono, email, sitio_web,
    financiamiento_anual, gasto_campana_ultima, fuente_financiamiento,
    historia_timeline,
    facebook_url, twitter_url, instagram_url,
    total_militantes, total_escaños,
    created_at
) VALUES 
-- Fuerza Popular
(
    'clxyz1000000001',
    'Fuerza Popular',
    'FP',
    'https://upload.wikimedia.org/wikipedia/commons/d/db/LogoFuerzaPopular.jpg',
    '#FF6600',
    true,
    'Alberto Fujimori',
    '2010-05-29',
    'Partido político peruano de derecha fundado por Alberto Fujimori',
    'Derecha conservadora',
    'Av. Salaverry 145, Jesús María, Lima',
    '01-4331234',
    'contacto@fuerzapopular.pe',
    'https://fuerzapopular.pe',
    15000000,
    25000000,
    'Fondos partidarios, aportes privados y recaudación en eventos' ,
    '[
        {"año": 2010, "evento": "Fundación de Fuerza 2011, origen del partido"},
        {"año": 2011, "evento": "Segunda vuelta presidencial con Keiko Fujimori"},
        {"año": 2016, "evento": "Mayoría absoluta en el Congreso"},
        {"año": 2021, "evento": "Tercera participación en segunda vuelta presidencial"},
        {"año": 2022, "evento": "Reestructuración interna del partido"}
    ]'::json,
    'https://facebook.com/fuerzapopular',
    'https://twitter.com/fuerzapopularpe',
    'https://instagram.com/fuerzapopular',
    150000,
    24,
    NOW()
),
-- Perú Libre
(
    'clxyz2000000002',
    'Perú Libre',
    'PL',
    'https://upload.wikimedia.org/wikipedia/commons/1/11/Per%C3%BA_Libre_logo.svg',
    '#FF0000',
    true,
    'Vladimir Cerrón',
    '2016-10-21',
    'Partido de izquierda que propone cambios estructurales en el Estado',
    'Izquierda socialista',
    'Jr. Washington 1234, Cercado de Lima',
    '01-4332345',
    'contacto@perulibre.pe',
    'https://perulibre.pe',
    NULL,
    NULL,
    'Aportes de militantes, actividades políticas y fondos de campaña',
    '[
        {"año": 2016, "evento": "Fundación del partido político en Junín por Vladimir Cerrón"},
        {"año": 2018, "evento": "Participación en elecciones regionales"},
        {"año": 2020, "evento": "Inscripción nacional ante el JNE"},
        {"año": 2021, "evento": "Victoria presidencial de Pedro Castillo"},
        {"año": 2022, "evento": "Crisis política y vacancia presidencial"},
        {"año": 2024, "evento": "Reestructuración interna y renovación de cuadros"}
    ]'::json,
    'https://facebook.com/perulibre',
    'https://twitter.com/perulibre',
    'https://instagram.com/perulibre',
    80000,
    37,
    NOW()
),
-- Acción Popular
(
    'clxyz3000000003',
    'Acción Popular',
    'AP',
    'https://upload.wikimedia.org/wikipedia/commons/e/ed/Acci%C3%B3n_Popular.png',
    '#FF0000',
    true,
    'Fernando Belaúnde Terry',
    '1956-07-07',
    'Partido histórico fundado por Fernando Belaúnde Terry',
    'Centro democrático',
    'Av. Alfonso Ugarte 1484, Cercado de Lima',
    '01-4333456',
    'contacto@accionpopular.pe',
    'https://accionpopular.pe',
    NULL,
    NULL,
    'Aportes voluntarios y financiamiento estatal directo',
    '[
        {"año": 1956, "evento": "Fundación por Fernando Belaúnde Terry"},
        {"año": 1963, "evento": "Primera elección de Belaúnde como presidente"},
        {"año": 1980, "evento": "Segundo gobierno de Belaúnde"},
        {"año": 2001, "evento": "Reinscripción del partido"},
        {"año": 2021, "evento": "Participación en elecciones generales"}
    ]'::json,
    'https://facebook.com/accionpopular',
    'https://twitter.com/accionpopular',
    'https://instagram.com/accionpopular',
    120000,
    15,
    NOW()
),
-- Alianza Para el Progreso
(
    'clxyz4000000004',
    'Alianza Para el Progreso',
    'APP',
    'https://upload.wikimedia.org/wikipedia/commons/3/3c/Alianza_para_el_Progreso_Peru.svg',
    '#0066CC',
    true,
    'César Acuña',
    '2001-12-08',
    'Partido político de centro fundado por César Acuña',
    'Centro progresista',
    'Av. Petit Thouars 4653, Miraflores, Lima',
    '01-4334567',
    'contacto@app.pe',
    'https://app.pe',
    NULL,
    NULL,
    'Fondos propios y aportes privados de militantes',
    '[
        {"año": 2001, "evento": "Fundación del partido por César Acuña"},
        {"año": 2014, "evento": "Participación en elecciones regionales"},
        {"año": 2016, "evento": "Primera candidatura presidencial"},
        {"año": 2021, "evento": "Participación en elecciones generales"},
        {"año": 2024, "evento": "Consolidación regional en el norte del país"}
    ]'::json,
    'https://facebook.com/apperu',
    'https://twitter.com/apperu',
    'https://instagram.com/apperu',
    100000,
    22,
    NOW()
),
-- Renovación Popular
(
    'clxyz5000000005',
    'Renovación Popular',
    'RP',
    'https://upload.wikimedia.org/wikipedia/commons/3/33/Logo_Renovaci%C3%B3n_Popular_2023.png',
    '#00AAFF',
    true,
    'Rafael López Aliaga',
    '2019-11-04',
    'Partido de derecha liberal fundado por Rafael López Aliaga',
    'Derecha liberal',
    'Av. Javier Prado Este 5268, La Molina, Lima',
    '01-4335678',
    'contacto@renovacionpopular.pe',
    'https://renovacionpopular.pe',
    NULL,
    NULL,
    'Aportes empresariales y contribuciones de simpatizantes',
    '[
        {"año": 2019, "evento": "Fundación del partido por Rafael López Aliaga"},
        {"año": 2020, "evento": "Inscripción en el Registro de Organizaciones Políticas"},
        {"año": 2021, "evento": "Participación en elecciones generales"},
        {"año": 2023, "evento": "Rafael López Aliaga asume la Alcaldía de Lima"}
    ]'::json,
    'https://facebook.com/renovacionpopular',
    'https://twitter.com/renovacionpopular',
    'https://instagram.com/renovacionpopular',
    60000,
    13,
    NOW()
);

-- =====================================================
-- 2. DISTRITOS ELECTORALES
-- =====================================================

INSERT INTO distrito (
    id, nombre, codigo, es_distrito_nacional,
    num_senadores, num_diputados, activo, created_at
) VALUES
('dist001', 'Lima', 'LIMA', false, 0, 36, true, NOW()),
('dist002', 'Arequipa', 'AQP', false, 0, 5, true, NOW()),
('dist003', 'La Libertad', 'LAL', false, 0, 8, true, NOW()),
('dist004', 'Cusco', 'CUS', false, 0, 5, true, NOW()),
('dist005', 'Piura', 'PIU', false, 0, 7, true, NOW()),
('dist006', 'Junín', 'JUN', false, 0, 5, true, NOW()),
('dist007', 'Lambayeque', 'LAM', false, 0, 5, true, NOW()),
('dist008', 'Nacional', 'NAC', true, 60, 0, true, NOW());

-- =====================================================
-- 3. PROCESO ELECTORAL
-- =====================================================

INSERT INTO procesoelectoral (
    id, nombre, año, fecha_elecciones, activo, created_at
) VALUES
('proc2021', 'Elecciones Generales 2021', 2021, '2021-04-11', false, NOW()),
('proc2026', 'Elecciones Generales 2026', 2026, '2026-04-11', true, NOW());

-- =====================================================
-- 4. PERSONAS (Políticos conocidos)
-- =====================================================
INSERT INTO persona (
    id, dni, nombres, apellidos, nombre_completo,
    foto_url, fecha_nacimiento, profesion, biografia_corta,
    educacion_tecnica, educacion_universitaria, grado_academico, titulo_profesional, post_grado,
    hoja_vida_url,
    experiencia_laboral,
    antecedentes_penales, antecedentes_judiciales,
    facebook_url, twitter_url, instagram_url,
    created_at
) VALUES
-- Keiko Fujimori
(
    'pers001',
    '09554634',
    'Keiko Sofía',
    'Fujimori Higuchi',
    'Keiko Sofía Fujimori Higuchi',
    NULL,
    '1975-05-25',
    'Administradora de Empresas',
    'Lideresa de Fuerza Popular y ex candidata presidencial en 2011, 2016 y 2021',
    NULL,
    'Boston University (MBA)',
    'Magíster en Administración de Empresas',
    'Master en Administración de Empresas',
    'Columbia University (Maestría en Administración Pública)',
    'https://example.com/hv/keiko-fujimori.pdf',
    '[
        {"cargo": "Congresista de la República", "empresa": "Congreso del Perú", "periodo": "2006 - 2011", "descripcion": "Representó a Lima; promovió proyectos de educación y familia."},
        {"cargo": "Presidenta del partido", "empresa": "Fuerza Popular", "periodo": "2010 - Actualidad", "descripcion": "Lidera el principal partido de oposición."}
    ]'::json,
    '[]'::json,
    '[]'::json,
    'https://facebook.com/keikofujimori',
    'https://twitter.com/keikofujimori',
    'https://instagram.com/keikofujimori',
    NOW()
),
-- Pedro Castillo
(
    'pers002',
    '42196397',
    'José Pedro',
    'Castillo Terrones',
    'José Pedro Castillo Terrones',
    NULL,
    '1969-10-19',
    'Profesor',
    'Ex presidente del Perú (2021-2022), profesor rural y líder sindical.',
    'Instituto Superior Pedagógico de Cajamarca (Educación Primaria)',
    'Universidad César Vallejo (Licenciatura en Educación)',
    'Licenciado en Educación',
    'Profesor de Educación Primaria',
    'Universidad César Vallejo (Maestría en Psicología Educativa)',
    'https://example.com/hv/pedro-castillo.pdf',
    '[
        {"cargo": "Profesor", "empresa": "Institución Educativa N°10465 Puña, Cajamarca", "periodo": "1995 - 2021", "descripcion": "Docente de primaria en zona rural."},
        {"cargo": "Dirigente sindical", "empresa": "Sindicato Unitario de Trabajadores de la Educación del Perú (SUTEP)", "periodo": "2017 - 2021", "descripcion": "Líder de la huelga magisterial de 2017."},
        {"cargo": "Presidente del Perú", "empresa": "Gobierno del Perú", "periodo": "2021 - 2022", "descripcion": "Mandato interrumpido tras crisis política."}
    ]'::json,
    '[]'::json,
    '[
        {"tipo": "Judicial", "descripcion": "Investigación por presunto delito de rebelión", "estado": "En proceso", "año": 2023}
    ]'::json,
    'https://facebook.com/pedrocastillo',
    'https://twitter.com/pedrocastillo',
    'https://instagram.com/pedrocastillo',
    NOW()
),
-- María del Carmen Alva
(
    'pers003',
    '09563872',
    'María del Carmen',
    'Alva Prieto',
    'María del Carmen Alva Prieto',
    NULL,
    '1965-04-23',
    'Administradora',
    'Ex presidenta del Congreso (2021-2022), congresista por Acción Popular.',
    NULL,
    'Universidad de Lima (Administración)',
    'Bachiller en Administración',
    'Licenciada en Administración',
    'Universidad de Navarra (Diplomado en Gerencia Pública)',
    'https://example.com/hv/maria-alva.pdf',
    '[
        {"cargo": "Gerente de Proyectos", "empresa": "Ministerio de Trabajo y Promoción del Empleo", "periodo": "2002 - 2006", "descripcion": "Gestión de programas de inserción laboral juvenil."},
        {"cargo": "Congresista de la República", "empresa": "Congreso del Perú", "periodo": "2021 - Actualidad", "descripcion": "Integrante de la Comisión de Constitución."}
    ]'::json,
    '[]'::json,
    '[]'::json,
    'https://facebook.com/mariaalva',
    'https://twitter.com/carmenaIvap',
    'https://instagram.com/mariaalva',
    NOW()
),
-- César Acuña
(
    'pers004',
    '17807070',
    'César Augusto',
    'Acuña Peralta',
    'César Augusto Acuña Peralta',
    NULL,
    '1952-11-11',
    'Empresario y educador',
    'Fundador de APP, ex alcalde de Trujillo y ex candidato presidencial.',
    'Instituto Superior Tecnológico Trujillo (Educación Técnica)',
    'Universidad Nacional de Trujillo (Educación)',
    'Doctor en Educación',
    'Doctor en Educación',
    'Universidad Complutense de Madrid (Doctorado en Educación)',
    'https://example.com/hv/cesar-acuna.pdf',
    '[
        {"cargo": "Fundador y Rector", "empresa": "Universidad César Vallejo", "periodo": "1991 - Actualidad", "descripcion": "Fundador y presidente del grupo educativo."},
        {"cargo": "Alcalde Provincial de Trujillo", "empresa": "Municipalidad Provincial de Trujillo", "periodo": "2007 - 2014", "descripcion": "Promovió proyectos de infraestructura educativa."},
        {"cargo": "Gobernador Regional de La Libertad", "empresa": "Gobierno Regional de La Libertad", "periodo": "2015 - 2016", "descripcion": "Inició obras de modernización regional."}
    ]'::json,
    '[]'::json,
    '[
        {"tipo": "Judicial", "descripcion": "Investigación por presunta compra de votos en el Congreso", "estado": "Archivado", "año": 2017}
    ]'::json,
    'https://facebook.com/cesaracuna',
    'https://twitter.com/cesaracunapy',
    'https://instagram.com/cesaracuna',
    NOW()
),
-- Rafael López Aliaga
(
    'pers005',
    '07938272',
    'Rafael Bernardo',
    'López Aliaga Cazorla',
    'Rafael Bernardo López Aliaga Cazorla',
    NULL,
    '1961-09-11',
    'Empresario',
    'Alcalde de Lima (2023-2026), fundador de Renovación Popular.',
    NULL,
    'Universidad de Lima (Ingeniería Industrial)',
    'Ingeniero Industrial',
    'Ingeniero Industrial',
    NULL,
    'https://example.com/hv/rafael-lopez.pdf',
    '[
        {"cargo": "Empresario", "empresa": "Grupo ACRES", "periodo": "1990 - Actualidad", "descripcion": "Fundador de empresas en sectores financiero y hotelero."},
        {"cargo": "Alcalde de Lima", "empresa": "Municipalidad Metropolitana de Lima", "periodo": "2023 - Actualidad", "descripcion": "Gestión urbana enfocada en transporte y seguridad ciudadana."}
    ]'::json,
    '[]'::json,
    '[
        {"tipo": "Judicial", "descripcion": "Investigación por presunto delito tributario", "estado": "Archivado", "año": 2004}
    ]'::json,
    'https://facebook.com/rafaellopezaliaga',
    'https://twitter.com/rlopezaliaga1',
    'https://instagram.com/rafaellopezaliaga',
    NOW()
),
-- Guido Bellido
(
    'pers006',
    '23904576',
    'Guido',
    'Bellido Ugarte',
    'Guido Bellido Ugarte',
    'https://live.staticflickr.com/65535/51339125796_58ae809cd2_5k.jpg',
    '1979-07-19',
    'Ingeniero Civil',
    'Ex primer ministro (2021), congresista por Perú Libre.',
    NULL,
    'Universidad Nacional del Altiplano (Ingeniería Civil)',
    'Bachiller en Ingeniería Civil',
    'Ingeniero Civil',
    'Universidad Nacional del Altiplano (Maestría en Gestión Pública)',
    'https://example.com/hv/guido-bellido.pdf',
    '[
        {"cargo": "Ingeniero de Obras", "empresa": "Gobierno Regional de Cusco", "periodo": "2005 - 2013", "descripcion": "Coordinación técnica de proyectos de infraestructura vial."},
        {"cargo": "Congresista de la República", "empresa": "Congreso del Perú", "periodo": "2021 - Actualidad", "descripcion": "Miembro de la Comisión de Energía y Minas."},
        {"cargo": "Presidente del Consejo de Ministros", "empresa": "Gobierno del Perú", "periodo": "2021", "descripcion": "Encabezó el gabinete ministerial durante los primeros meses de gobierno de Pedro Castillo."}
    ]'::json,
    '[]'::json,
    '[
        {"tipo": "Judicial", "descripcion": "Investigación por presunta apología al terrorismo", "estado": "En investigación", "año": 2021}
    ]'::json,
    'https://facebook.com/guidobellido',
    'https://twitter.com/GuidoBellido',
    'https://instagram.com/guidobellido',
    NOW()
),
(
    'pers007',
    '40781234',
    'Ana Lucía',
    'Herrera Valdivia',
    'Ana Lucía Herrera Valdivia',
    NULL,
    '1978-02-14',
    'Abogada',
    'Senadora por Lima, especializada en derecho constitucional.',
    NULL,
    'Pontificia Universidad Católica del Perú (Derecho)',
    'Bachiller en Derecho',
    'Abogada',
    'Universidad de Salamanca (Maestría en Derecho Constitucional)',
    'https://example.com/hv/ana-herrera.pdf',
    '[
        {"cargo": "Asesora Legal", "empresa": "Ministerio de Justicia", "periodo": "2005 - 2015", "descripcion": "Elaboración de dictámenes y proyectos de ley."},
        {"cargo": "Senadora", "empresa": "Congreso del Perú", "periodo": "2021 - Actualidad", "descripcion": "Miembro de la Comisión de Justicia y Derechos Humanos."}
    ]'::json,
    '[]'::json,
    '[]'::json,
    'https://facebook.com/anaherrerav',
    'https://twitter.com/anaherrerav',
    'https://instagram.com/anaherrerav',
    NOW()
),
-- Diego Ramos - Senador
(
    'pers008',
    '45873211',
    'Diego',
    'Ramos Salazar',
    'Diego Ramos Salazar',
    NULL,
    '1981-06-09',
    'Economista',
    'Senador por Arequipa, experto en políticas fiscales.',
    'Instituto de Comercio Exterior (Economía Aplicada)',
    'Universidad del Pacífico (Economía)',
    'Licenciado en Economía',
    'Economista',
    'Universidad de Chicago (Maestría en Políticas Públicas)',
    'https://example.com/hv/diego-ramos.pdf',
    '[
        {"cargo": "Analista Económico", "empresa": "Banco Central de Reserva del Perú", "periodo": "2006 - 2016", "descripcion": "Evaluación de impacto macroeconómico de políticas fiscales."},
        {"cargo": "Senador", "empresa": "Congreso del Perú", "periodo": "2021 - Actualidad", "descripcion": "Presidente de la Comisión de Economía."}
    ]'::json,
    '[]'::json,
    '[
        {
        "tipo": "Judicial",
        "descripcion": "Investigación por presunto conflicto de interés relacionada con adjudicaciones públicas; procedimiento archivado",
        "estado": "Archivado",
        "año": 2014
        }
    ]'::json,
    'https://facebook.com/diegoramos',
    'https://twitter.com/diegoramos',
    'https://instagram.com/diegoramos',
    NOW()
),
-- Carmen Vásquez - Diputada
(
    'pers009',
    '43128765',
    'Carmen Rosa',
    'Vásquez Torres',
    'Carmen Rosa Vásquez Torres',
    NULL,
    '1985-03-12',
    'Docente',
    'Diputada por Piura, defensora de la educación rural.',
    'Instituto Pedagógico Nacional Monterrico (Educación Primaria)',
    'Universidad Nacional de Piura (Educación)',
    'Licenciada en Educación',
    'Profesora de Educación Primaria',
    NULL,
    'https://example.com/hv/carmen-vasquez.pdf',
    '[
        {"cargo": "Docente", "empresa": "Ministerio de Educación", "periodo": "2008 - 2021", "descripcion": "Educadora en instituciones rurales de Piura."},
        {"cargo": "Diputada", "empresa": "Congreso del Perú", "periodo": "2021 - Actualidad", "descripcion": "Miembro de la Comisión de Educación y Cultura."}
    ]'::json,
    '[
        {
        "tipo": "Penal/Administrativo",
        "descripcion": "Multa administrativa por incumplimiento de norma técnica en obra pública (sanción administrativa)",
        "estado": "Archivado",
        "año": 2012
        }
    ]'::json,
    '[]'::json,
    'https://facebook.com/carmenvasquez',
    'https://twitter.com/carmenvasquez',
    'https://instagram.com/carmenvasquez',
    NOW()
),
-- Luis Gamarra - Diputado
(
    'pers010',
    '40291833',
    'Luis Alberto',
    'Gamarra Ramos',
    'Luis Alberto Gamarra Ramos',
    NULL,
    '1972-09-22',
    'Ingeniero Industrial',
    'Diputado por Cusco, impulsor de políticas de infraestructura.',
    NULL,
    'Universidad Nacional de Ingeniería (Ingeniería Industrial)',
    'Ingeniero Industrial',
    'Ingeniero Industrial',
    'Pontificia Universidad Católica del Perú (Diplomado en Gestión Pública)',
    'https://example.com/hv/luis-gamarra.pdf',
    '[
        {"cargo": "Gerente de Proyectos", "empresa": "Ministerio de Transportes y Comunicaciones", "periodo": "2000 - 2014", "descripcion": "Supervisión de proyectos viales en el sur del país."},
        {"cargo": "Diputado", "empresa": "Congreso del Perú", "periodo": "2021 - Actualidad", "descripcion": "Vicepresidente de la Comisión de Infraestructura."}
    ]'::json,
    '[]'::json,
    '[]'::json,
    'https://facebook.com/luisgamarra',
    'https://twitter.com/luisgamarra',
    'https://instagram.com/luisgamarra',
    NOW()
);

-- =====================================================
-- 5. LEGISLADORES (Periodo 2021-2026)
-- =====================================================

INSERT INTO legislador (
    id, persona_id, partido_id, distrito_id,
    camara, periodo_inicio, periodo_fin,
    esta_activo, email_congreso, created_at
) VALUES
-- Keiko Fujimori - Congresista por Lima
(
    'leg001',
    'pers001',
    'clxyz1000000001',
    'dist001',
    'CONGRESO',
    '2021-07-28',
    '2026-07-27',
    true,
    'kfujimori@congreso.gob.pe',
    NOW()
),
-- Guido Bellido - Congresista por Cusco
(
    'leg002',
    'pers006',
    'clxyz2000000002',
    'dist004',
    'CONGRESO',
    '2021-07-28',
    '2026-07-27',
    true,
    'gbellido@congreso.gob.pe',
    NOW()
),
-- María del Carmen Alva - Congresista por Lima
(
    'leg003',
    'pers003',
    'clxyz3000000003',
    'dist001',
    'CONGRESO',
    '2021-07-28',
    '2026-07-27',
    true,
    'malva@congreso.gob.pe',
    NOW()
);

-- =====================================================
-- 6. CANDIDATOS (Elecciones 2021)
-- =====================================================

INSERT INTO candidato (
    id, persona_id, proceso_electoral_id, tipo,
    partido_id, distrito_id, numero_lista,
    propuestas, plan_gobierno_url,
    estado, votos_obtenidos, fue_elegido, created_at
) VALUES
-- Keiko Fujimori - Candidata Presidencial 2021
(
    'cand001',
    'pers001',
    'proc2021',
    'PRESIDENTE',
    'clxyz1000000001',
    NULL,
    1,
    'Reactivación económica, lucha contra la corrupción, inversión en educación y salud',
    'https://example.com/planes/fp-2021.pdf',
    'HABIL',
    8792117,
    false,
    NOW()
),
-- Pedro Castillo - Candidato Presidencial 2021
(
    'cand002',
    'pers002',
    'proc2021',
    'PRESIDENTE',
    'clxyz2000000002',
    NULL,
    1,
    'Nueva constitución, renegociación de contratos mineros, segunda reforma agraria',
    'https://example.com/planes/pl-2021.pdf',
    'HABIL',
    8836380,
    true,
    NOW()
),
-- César Acuña - Candidato Presidencial 2021
(
    'cand003',
    'pers004',
    'proc2021',
    'PRESIDENTE',
    'clxyz4000000004',
    NULL,
    1,
    'Bono universal familiar, reactivación económica, infraestructura',
    'https://example.com/planes/app-2021.pdf',
    'HABIL',
    934664,
    false,
    NOW()
),
-- Rafael López Aliaga - Candidato Presidencial 2021
(
    'cand004',
    'pers005',
    'proc2021',
    'PRESIDENTE',
    'clxyz5000000005',
    NULL,
    1,
    'Liberalismo económico, reducción del Estado, inversión privada',
    'https://example.com/planes/rp-2021.pdf',
    'HABIL',
    1336221,
    false,
    NOW()
),
(
    'cand005',
    'pers007',
    'proc2021',
    'SENADOR',
    'clxyz4000000004',
    'dist001',
    2,
    'Reforma judicial, fortalecimiento del sistema anticorrupción, igualdad de género',
    'https://example.com/planes/app-senado.pdf',
    'HABIL',
    154320,
    true,
    NOW()
),
-- Diego Ramos - Senador por Arequipa (Renovación Popular)
(
    'cand006',
    'pers008',
    'proc2021',
    'SENADOR',
    'clxyz5000000005',
    'dist002',
    3,
    'Reactivación económica descentralizada, incentivos tributarios para regiones del sur',
    'https://example.com/planes/rp-senado.pdf',
    'HABIL',
    120450,
    false,
    NOW()
),
-- Carmen Vásquez - Diputada por Piura (Perú Libre)
(
    'cand007',
    'pers009',
    'proc2021',
    'DIPUTADO',
    'clxyz2000000002',
    'dist003',
    5,
    'Educación inclusiva, conectividad digital en zonas rurales, derechos docentes',
    'https://example.com/planes/pl-diputados.pdf',
    'HABIL',
    100230,
    true,
    NOW()
),
-- Luis Gamarra - Diputado por Cusco (Acción Popular)
(
    'cand008',
    'pers010',
    'proc2021',
    'DIPUTADO',
    'clxyz3000000003',
    'dist004',
    4,
    'Infraestructura vial sostenible, turismo responsable, desarrollo regional',
    'https://example.com/planes/ap-diputados.pdf',
    'HABIL',
    95410,
    false,
    NOW()
);

-- =====================================================
-- 7. PROYECTOS DE LEY (Ejemplos)
-- =====================================================

INSERT INTO proyectoley (
    id, legislador_id, numero, titulo, resumen,
    fecha_presentacion, estado, url_documento, created_at
) VALUES
(
    'proy001',
    'leg001',
    '01234/2021-CR',
    'Ley de fortalecimiento de la seguridad ciudadana',
    'Propone incrementar las penas por delitos contra el patrimonio y fortalecer las capacidades de la Policía Nacional del Perú',
    '2021-09-15',
    'En comisión',
    'https://example.com/proyectos/01234-2021.pdf',
    NOW()
),
(
    'proy002',
    'leg003',
    '01567/2021-CR',
    'Ley de promoción de la educación rural',
    'Busca mejorar la infraestructura educativa en zonas rurales y aumentar los salarios de docentes en estas áreas',
    '2021-10-20',
    'Aprobado',
    'https://example.com/proyectos/01567-2021.pdf',
    NOW()
),
(
    'proy003',
    'leg002',
    '01789/2022-CR',
    'Ley de transparencia en la gestión pública',
    'Establece mecanismos de control ciudadano y rendición de cuentas en todas las entidades del Estado',
    '2022-03-10',
    'Archivado',
    'https://example.com/proyectos/01789-2022.pdf',
    NOW()
);

-- =====================================================
-- 8. ASISTENCIAS (Ejemplos)
-- =====================================================

INSERT INTO asistencia (
    id, legislador_id, fecha, tipo_sesion, asistio, created_at
) VALUES
('asis001', 'leg001', '2024-01-15', 'Pleno', true, NOW()),
('asis002', 'leg001', '2024-01-22', 'Comisión', true, NOW()),
('asis003', 'leg001', '2024-01-29', 'Pleno', false, NOW()),
('asis004', 'leg002', '2024-01-15', 'Pleno', true, NOW()),
('asis005', 'leg002', '2024-01-22', 'Comisión', true, NOW()),
('asis006', 'leg003', '2024-01-15', 'Pleno', true, NOW()),
('asis007', 'leg003', '2024-01-22', 'Comisión', true, NOW()),
('asis008', 'leg003', '2024-01-29', 'Pleno', true, NOW());

-- =====================================================
-- 9. DENUNCIAS (Ejemplos)
-- =====================================================

INSERT INTO denuncia (
    id, legislador_id, titulo, descripcion, tipo,
    fecha_denuncia, estado, resolucion, url_documento, created_at
) VALUES
(
    'den001',
    'leg001',
    'Investigación por presunto lavado de activos',
    'Fiscalía investiga presuntas irregularidades en el manejo de fondos de campaña',
    'Penal',
    '2023-05-10',
    'En investigación',
    NULL,
    'https://example.com/denuncias/den001.pdf',
    NOW()
),
(
    'den002',
    'leg002',
    'Denuncia constitucional por apología al terrorismo',
    'Cuestionamientos por declaraciones públicas relacionadas con grupos terroristas',
    'Constitucional',
    '2023-08-15',
    'Desestimado',
    'El Congreso desestimó la denuncia por falta de elementos probatorios',
    'https://example.com/denuncias/den002.pdf',
    NOW()
);

-- =====================================================
-- FIN DEL SEED
-- =====================================================

-- Verificar datos insertados
SELECT 'Partidos insertados:' as info, COUNT(*) as total FROM partidopolitico
UNION ALL
SELECT 'Distritos insertados:', COUNT(*) FROM distrito
UNION ALL
SELECT 'Personas insertadas:', COUNT(*) FROM persona
UNION ALL
SELECT 'Legisladores insertados:', COUNT(*) FROM legislador
UNION ALL
SELECT 'Candidatos insertados:', COUNT(*) FROM candidato
UNION ALL
SELECT 'Proyectos de ley insertados:', COUNT(*) FROM proyectoley
UNION ALL
SELECT 'Asistencias insertadas:', COUNT(*) FROM asistencia
UNION ALL
SELECT 'Denuncias insertadas:', COUNT(*) FROM denuncia;