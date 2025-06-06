// authGuard.js

function getDecodedToken() {
  const token = localStorage.getItem("access_token");
  if (!token) {
    window.location.href = "inicio-sesion.html";
    return null;
  }

  try {
    return jwt_decode(token);
  } catch (e) {
    localStorage.removeItem("access_token");
    window.location.href = "inicio-sesion.html";
    return null;
  }
}

function protegerRuta(tipoEsperado) {
  const decoded = getDecodedToken();
  if (!decoded) return;

  const esProfesor = decoded.es_profesor;

  if (tipoEsperado === "profesor" && !esProfesor) {
    window.location.href = "perfilEstudiante.html";
  }
  if (tipoEsperado === "estudiante" && esProfesor) {
    window.location.href = "perfilProfesor.html";
  }
}

function redirigirMenuPorRol(rutasPorRol) {
  const decoded = getDecodedToken();
  if (!decoded) return;

  const esProfesor = decoded.es_profesor;
  const rol = esProfesor ? "profesor" : "estudiante";

  const rutas = rutasPorRol[rol];

  document.getElementById("btn-pagina-principal").href = rutas.paginaPrincipal;
  document.getElementById("btn-avances").href = rutas.avances;
  document.getElementById("btn-habilidades").href = rutas.habilidades;
  document.getElementById("btn-maratones").href = rutas.maratones;
  document.getElementById("btn-perfil").href = rutas.perfil;
}
