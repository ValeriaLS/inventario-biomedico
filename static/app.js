// ============================================
// INVENTARIO BIOMÉDICO
// Funciones para interactuar con la API
// ============================================

const formulario = document.getElementById("formulario-equipo");
const listaEquipos = document.getElementById("lista-equipos");
const mensaje = document.getElementById("mensaje");
const botonActualizar = document.getElementById("btn-actualizar");
const botonReporte = document.getElementById("btn-reporte");
const resultadoReporte = document.getElementById("resultado-reporte");

let equipoEnEdicion = null;


// ============================================
// MOSTRAR MENSAJES
// ============================================

function mostrarMensaje(texto, tipo = "exito") {
    mensaje.textContent = texto;

    mensaje.style.color =
        tipo === "error" ? "#c74747" : "#21865b";
}


// ============================================
// CONSULTAR Y MOSTRAR EQUIPOS
// ============================================

async function cargarEquipos() {
    listaEquipos.replaceChildren();

    const filaCarga = document.createElement("tr");
    const celdaCarga = document.createElement("td");

    celdaCarga.colSpan = 7;
    celdaCarga.textContent = "Cargando equipos...";

    filaCarga.appendChild(celdaCarga);
    listaEquipos.appendChild(filaCarga);

    try {
        const respuesta = await fetch("/equipos");

        if (!respuesta.ok) {
            throw new Error("No se pudieron consultar los equipos.");
        }

        const equipos = await respuesta.json();

        listaEquipos.replaceChildren();

        if (equipos.length === 0) {
            const fila = document.createElement("tr");
            const celda = document.createElement("td");

            celda.colSpan = 7;
            celda.textContent = "Todavía no hay equipos registrados.";

            fila.appendChild(celda);
            listaEquipos.appendChild(fila);

            return;
        }

        equipos.forEach((equipo) => {
            const fila = document.createElement("tr");

            // Datos del equipo
            agregarCelda(fila, equipo.nombre);
            agregarCelda(fila, equipo.marca);
            agregarCelda(fila, equipo.modelo);
            agregarCelda(fila, equipo.numero_serie);
            agregarCelda(fila, equipo.ubicacion);

            // Estado con color
            const celdaEstado = document.createElement("td");
            const etiquetaEstado = document.createElement("span");

            etiquetaEstado.textContent = equipo.estado;
            etiquetaEstado.classList.add("estado");

            if (equipo.estado === "Disponible") {
                etiquetaEstado.classList.add("estado-disponible");
            } else if (equipo.estado === "En mantenimiento") {
                etiquetaEstado.classList.add("estado-mantenimiento");
            } else {
                etiquetaEstado.classList.add("estado-fuera");
            }

            celdaEstado.appendChild(etiquetaEstado);
            fila.appendChild(celdaEstado);

            // Botones de acciones
            const celdaAcciones = document.createElement("td");
            const contenedorAcciones = document.createElement("div");

            contenedorAcciones.classList.add("acciones");

            const botonEditar = document.createElement("button");
            botonEditar.type = "button";
            botonEditar.textContent = "Editar";
            botonEditar.classList.add("btn-editar");

            botonEditar.addEventListener("click", () => {
                editarEquipo(equipo);
            });

            const botonEliminar = document.createElement("button");
            botonEliminar.type = "button";
            botonEliminar.textContent = "Eliminar";
            botonEliminar.classList.add("btn-eliminar");

            botonEliminar.addEventListener("click", () => {
                eliminarEquipo(equipo);
            });

            contenedorAcciones.appendChild(botonEditar);
            contenedorAcciones.appendChild(botonEliminar);

            celdaAcciones.appendChild(contenedorAcciones);
            fila.appendChild(celdaAcciones);

            listaEquipos.appendChild(fila);
        });

    } catch (error) {
        listaEquipos.replaceChildren();

        const fila = document.createElement("tr");
        const celda = document.createElement("td");

        celda.colSpan = 7;
        celda.textContent = error.message;

        fila.appendChild(celda);
        listaEquipos.appendChild(fila);
    }
}


// ============================================
// CREAR CELDAS DE LA TABLA
// ============================================

function agregarCelda(fila, contenido) {
    const celda = document.createElement("td");

    celda.textContent = contenido ?? "";

    fila.appendChild(celda);
}


// ============================================
// REGISTRAR O ACTUALIZAR EQUIPO
// ============================================

formulario.addEventListener("submit", async (evento) => {
    evento.preventDefault();

    const datos = {
        nombre: formulario.nombre.value.trim(),
        marca: formulario.marca.value.trim(),
        modelo: formulario.modelo.value.trim(),
        numero_serie: formulario.numero_serie.value.trim(),
        ubicacion: formulario.ubicacion.value.trim(),
        estado: formulario.estado.value
    };

    const editando = equipoEnEdicion !== null;

    const url = editando
        ? `/equipos/${encodeURIComponent(equipoEnEdicion)}`
        : "/equipos";

    const metodo = editando ? "PUT" : "POST";

    const botonEnviar = formulario.querySelector(
        'button[type="submit"]'
    );

    botonEnviar.disabled = true;

    try {
        const respuesta = await fetch(url, {
            method: metodo,
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(datos)
        });

        const resultado = await respuesta.json();

        if (!respuesta.ok) {
            const detalle = resultado.detail;

            let textoError = "No se pudo guardar el equipo.";

            if (typeof detalle === "string") {
                textoError = detalle;
            } else if (Array.isArray(detalle)) {
                textoError = detalle
                    .map((error) => error.msg)
                    .join(". ");
            }

            throw new Error(textoError);
        }

        mostrarMensaje(
            editando
                ? "¡Equipo actualizado correctamente!"
                : "¡Equipo registrado correctamente!"
        );

        formulario.reset();
        equipoEnEdicion = null;

        botonEnviar.textContent = "Registrar equipo";

        await cargarEquipos();

    } catch (error) {
        mostrarMensaje(error.message, "error");
    } finally {
        botonEnviar.disabled = false;
    }
});


// ============================================
// EDITAR EQUIPO
// ============================================

function editarEquipo(equipo) {
    equipoEnEdicion = equipo.id;

    formulario.nombre.value = equipo.nombre;
    formulario.marca.value = equipo.marca;
    formulario.modelo.value = equipo.modelo;
    formulario.numero_serie.value = equipo.numero_serie;
    formulario.ubicacion.value = equipo.ubicacion;
    formulario.estado.value = equipo.estado;

    const botonEnviar = formulario.querySelector(
        'button[type="submit"]'
    );

    botonEnviar.textContent = "Guardar cambios";

    mostrarMensaje(
        "Estás editando un equipo. Modifica los campos y guarda los cambios.",
        "exito"
    );

    formulario.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}


// ============================================
// ELIMINAR EQUIPO
// ============================================

async function eliminarEquipo(equipo) {
    const confirmar = window.confirm(
        `¿Estás segura de que deseas eliminar el equipo "${equipo.nombre}"?`
    );

    if (!confirmar) {
        return;
    }

    try {
        const respuesta = await fetch(
            `/equipos/${encodeURIComponent(equipo.id)}`,
            {
                method: "DELETE"
            }
        );

        if (!respuesta.ok) {
            const resultado = await respuesta.json();

            throw new Error(
                resultado.detail || "No se pudo eliminar el equipo."
            );
        }

        mostrarMensaje("El equipo se eliminó correctamente.");

        // Si se estaba editando el equipo eliminado, limpiar el formulario.
        if (equipoEnEdicion === equipo.id) {
            formulario.reset();
            equipoEnEdicion = null;

            formulario.querySelector(
                'button[type="submit"]'
            ).textContent = "Registrar equipo";
        }

        await cargarEquipos();

    } catch (error) {
        mostrarMensaje(error.message, "error");
    }
}


// ============================================
// ACTUALIZAR LISTA
// ============================================

botonActualizar.addEventListener("click", () => {
    cargarEquipos();
});


// ============================================
// GENERAR REPORTE
// ============================================

botonReporte.addEventListener("click", async () => {
    botonReporte.disabled = true;
    botonReporte.textContent = "Generando reporte...";

    resultadoReporte.style.display = "block";
    resultadoReporte.textContent = "Consultando información del inventario...";

    try {
        const respuesta = await fetch("/reportes/simulado", {
            method: "POST"
        });

        const reporte = await respuesta.json();

        if (!respuesta.ok) {
            throw new Error(
                reporte.detail || "No se pudo generar el reporte."
            );
        }

        resultadoReporte.textContent =
            "REPORTE DEL INVENTARIO BIOMÉDICO\n\n" +
            `Total de equipos: ${reporte.total_equipos}\n` +
            `Equipos disponibles: ${reporte.disponibles}\n` +
            `Equipos en mantenimiento: ${reporte.en_mantenimiento}`;

        // Mostrar también la cantidad de equipos fuera de servicio
        // si la API incluye este dato.
        if (reporte.fuera_de_servicio !== undefined) {
            resultadoReporte.textContent +=
                `\nEquipos fuera de servicio: ${reporte.fuera_de_servicio}`;
        }

    } catch (error) {
        resultadoReporte.textContent =
            `Error al generar el reporte: ${error.message}`;

    } finally {
        botonReporte.disabled = false;
        botonReporte.textContent = "Generar reporte";
    }
});


// ============================================
// INICIAR APLICACIÓN
// ============================================

cargarEquipos();