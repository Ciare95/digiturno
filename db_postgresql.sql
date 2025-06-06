CREATE TABLE "usuarios" (
  "id" INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "nombre" varchar(100) NOT NULL,
  "apellido" varchar(100) NOT NULL,
  "email" varchar(255) UNIQUE NOT NULL,
  "telefono" varchar(15),
  "cedula" varchar(20) UNIQUE,
  "password_hash" varchar(255) NOT NULL,
  "fecha_registro" timestamp DEFAULT (now()),
  "activo" boolean DEFAULT true,
  "ultimo_acceso" timestamp,
  "created_at" timestamp DEFAULT (now()),
  "updated_at" timestamp DEFAULT (now())
);

CREATE TABLE "empleados" (
  "id" INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "usuario_id" integer,
  "codigo_empleado" varchar(20) UNIQUE NOT NULL,
  "sucursal_id" integer,
  "ventanilla_asignada" varchar(10),
  "estado_conexion" varchar(20) DEFAULT 'desconectado',
  "fecha_ingreso" date,
  "activo" boolean DEFAULT true,
  "configuracion_ui" json,
  "created_at" timestamp DEFAULT (now()),
  "updated_at" timestamp DEFAULT (now())
);

CREATE TABLE "administradores" (
  "id" INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "usuario_id" integer,
  "nivel_acceso" varchar(20) DEFAULT 'admin',
  "permisos" json,
  "sucursal_id" integer,
  "activo" boolean DEFAULT true,
  "created_at" timestamp DEFAULT (now()),
  "updated_at" timestamp DEFAULT (now())
);

CREATE TABLE "sucursales" (
  "id" INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "nombre" varchar(100) NOT NULL,
  "direccion" text,
  "telefono" varchar(15),
  "ciudad" varchar(50),
  "departamento" varchar(50),
  "codigo_sucursal" varchar(10) UNIQUE NOT NULL,
  "activa" boolean DEFAULT true,
  "configuracion" json,
  "created_at" timestamp DEFAULT (now()),
  "updated_at" timestamp DEFAULT (now())
);

CREATE TABLE "servicios" (
  "id" INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "nombre" varchar(100) NOT NULL,
  "descripcion" text,
  "sucursal_id" integer,
  "codigo_servicio" varchar(10) NOT NULL,
  "tiempo_estimado_atencion" integer DEFAULT 15,
  "activo" boolean DEFAULT true,
  "orden_visualizacion" integer DEFAULT 0,
  "color_identificacion" varchar(7),
  "icono" varchar(50),
  "created_at" timestamp DEFAULT (now()),
  "updated_at" timestamp DEFAULT (now())
);

CREATE TABLE "turnos" (
  "id" INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "numero_turno" varchar(20) NOT NULL,
  "usuario_id" integer,
  "servicio_id" integer,
  "sucursal_id" integer,
  "empleado_id" integer,
  "estado" varchar(20) DEFAULT 'en_espera',
  "prioridad" integer DEFAULT 0,
  "fecha_creacion" timestamp DEFAULT (now()),
  "fecha_llamado" timestamp,
  "fecha_inicio_atencion" timestamp,
  "fecha_finalizacion" timestamp,
  "tiempo_espera_estimado" integer,
  "es_agendado" boolean DEFAULT false,
  "fecha_agendada" timestamp,
  "observaciones" text,
  "created_at" timestamp DEFAULT (now()),
  "updated_at" timestamp DEFAULT (now())
);

CREATE TABLE "calificaciones_servicio" (
  "id" INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "turno_id" integer,
  "usuario_id" integer,
  "empleado_id" integer,
  "servicio_id" integer,
  "calificacion" integer NOT NULL,
  "comentario" text,
  "aspectos_evaluados" json,
  "fecha_calificacion" timestamp DEFAULT (now()),
  "created_at" timestamp DEFAULT (now())
);

CREATE TABLE "configuraciones_sistema" (
  "id" INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "clave" varchar(100) UNIQUE NOT NULL,
  "valor" text NOT NULL,
  "descripcion" text,
  "tipo" varchar(20) DEFAULT 'string',
  "sucursal_id" integer,
  "categoria" varchar(50) DEFAULT 'general',
  "activa" boolean DEFAULT true,
  "created_at" timestamp DEFAULT (now()),
  "updated_at" timestamp DEFAULT (now())
);

CREATE TABLE "sesiones_usuario" (
  "id" INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "usuario_id" integer,
  "token" varchar(255) UNIQUE NOT NULL,
  "tipo_sesion" varchar(20) NOT NULL,
  "direccion_ip" varchar(45),
  "user_agent" text,
  "fecha_inicio" timestamp DEFAULT (now()),
  "fecha_expiracion" timestamp NOT NULL,
  "activa" boolean DEFAULT true,
  "created_at" timestamp DEFAULT (now())
);

CREATE TABLE "estadisticas_empleado" (
  "id" INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "empleado_id" integer,
  "fecha" date NOT NULL,
  "turnos_atendidos" integer DEFAULT 0,
  "tiempo_promedio_atencion" integer DEFAULT 0,
  "calificacion_promedio" decimal(3,2) DEFAULT 0,
  "tiempo_conectado" integer DEFAULT 0,
  "turnos_transferidos" integer DEFAULT 0,
  "created_at" timestamp DEFAULT (now()),
  "updated_at" timestamp DEFAULT (now())
);

CREATE TABLE "cola_turnos" (
  "id" INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "turno_id" integer,
  "servicio_id" integer,
  "posicion_cola" integer NOT NULL,
  "fecha_ingreso_cola" timestamp DEFAULT (now()),
  "tiempo_espera_estimado" integer,
  "activo" boolean DEFAULT true,
  "created_at" timestamp DEFAULT (now()),
  "updated_at" timestamp DEFAULT (now())
);

CREATE TABLE "notificaciones" (
  "id" INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "usuario_id" integer,
  "turno_id" integer,
  "tipo" varchar(30) NOT NULL,
  "titulo" varchar(100) NOT NULL,
  "mensaje" text NOT NULL,
  "leida" boolean DEFAULT false,
  "fecha_envio" timestamp DEFAULT (now()),
  "fecha_lectura" timestamp,
  "canal" varchar(20) DEFAULT 'websocket',
  "created_at" timestamp DEFAULT (now())
);

CREATE TABLE "auditoria" (
  "id" INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "tabla_afectada" varchar(50) NOT NULL,
  "registro_id" integer NOT NULL,
  "accion" varchar(20) NOT NULL,
  "datos_anteriores" json,
  "datos_nuevos" json,
  "usuario_id" integer,
  "direccion_ip" varchar(45),
  "fecha_accion" timestamp DEFAULT (now())
);

ALTER TABLE "empleados" ADD FOREIGN KEY ("usuario_id") REFERENCES "usuarios" ("id");

ALTER TABLE "empleados" ADD FOREIGN KEY ("sucursal_id") REFERENCES "sucursales" ("id");

ALTER TABLE "administradores" ADD FOREIGN KEY ("usuario_id") REFERENCES "usuarios" ("id");

ALTER TABLE "administradores" ADD FOREIGN KEY ("sucursal_id") REFERENCES "sucursales" ("id");

ALTER TABLE "servicios" ADD FOREIGN KEY ("sucursal_id") REFERENCES "sucursales" ("id");

ALTER TABLE "turnos" ADD FOREIGN KEY ("usuario_id") REFERENCES "usuarios" ("id");

ALTER TABLE "turnos" ADD FOREIGN KEY ("servicio_id") REFERENCES "servicios" ("id");

ALTER TABLE "turnos" ADD FOREIGN KEY ("sucursal_id") REFERENCES "sucursales" ("id");

ALTER TABLE "turnos" ADD FOREIGN KEY ("empleado_id") REFERENCES "empleados" ("id");

ALTER TABLE "calificaciones_servicio" ADD FOREIGN KEY ("turno_id") REFERENCES "turnos" ("id");

ALTER TABLE "calificaciones_servicio" ADD FOREIGN KEY ("usuario_id") REFERENCES "usuarios" ("id");

ALTER TABLE "calificaciones_servicio" ADD FOREIGN KEY ("empleado_id") REFERENCES "empleados" ("id");

ALTER TABLE "calificaciones_servicio" ADD FOREIGN KEY ("servicio_id") REFERENCES "servicios" ("id");

ALTER TABLE "configuraciones_sistema" ADD FOREIGN KEY ("sucursal_id") REFERENCES "sucursales" ("id");

ALTER TABLE "sesiones_usuario" ADD FOREIGN KEY ("usuario_id") REFERENCES "usuarios" ("id");

ALTER TABLE "estadisticas_empleado" ADD FOREIGN KEY ("empleado_id") REFERENCES "empleados" ("id");

ALTER TABLE "cola_turnos" ADD FOREIGN KEY ("turno_id") REFERENCES "turnos" ("id");

ALTER TABLE "cola_turnos" ADD FOREIGN KEY ("servicio_id") REFERENCES "servicios" ("id");

ALTER TABLE "notificaciones" ADD FOREIGN KEY ("usuario_id") REFERENCES "usuarios" ("id");

ALTER TABLE "notificaciones" ADD FOREIGN KEY ("turno_id") REFERENCES "turnos" ("id");

ALTER TABLE "auditoria" ADD FOREIGN KEY ("usuario_id") REFERENCES "usuarios" ("id");
