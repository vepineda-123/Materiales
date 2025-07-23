import streamlit as st
import pandas as pd
from datetime import datetime, date
import matplotlib.pyplot as plt

# Configuración de la página
st.set_page_config(
    page_title="Laboratorio de Materiales",
    page_icon="🏗",
    layout="wide"
)

# Título principal
st.title("🏗 Ensayos de Compresión de Cilindros de Concreto")
st.subheader("Laboratorio de Materiales - Resultados Confidenciales")

# Inicializar datos en session state
if 'ensayos' not in st.session_state:
    st.session_state.ensayos = []

# Sidebar para entrada de datos
st.sidebar.header("Registro de Nuevo Ensayo")

with st.sidebar:
    st.write("### Datos del Ensayo")
    
    # Formulario
    id_cilindro = st.text_input("ID del Cilindro:", placeholder="Ej: CIL-001")
    resistencia = st.number_input("Resistencia (MPa):", min_value=0.0, max_value=100.0, step=0.1, value=0.0)
    fecha_ensayo = st.date_input("Fecha del Ensayo:", value=date.today())
    
    if st.button("➕ Agregar Ensayo"):
        if id_cilindro and resistencia > 0:
            # Verificar si el ID ya existe
            ids_existentes = [ensayo['id'] for ensayo in st.session_state.ensayos]
            if id_cilindro in ids_existentes:
                st.error("⚠ Este ID ya existe")
            else:
                # Agregar nuevo ensayo
                nuevo_ensayo = {
                    'id': id_cilindro,
                    'resistencia': resistencia,
                    'fecha': fecha_ensayo
                }
                st.session_state.ensayos.append(nuevo_ensayo)
                st.success("✅ Ensayo agregado")
                st.rerun()
        else:
            st.error("❌ Complete todos los campos")

# Área principal
if st.session_state.ensayos:
    
    # Mostrar datos en tabla
    st.header("📋 Resultados de Ensayos")
    
    # Crear DataFrame para mostrar
    df_datos = pd.DataFrame([
        {
            'ID Cilindro': ensayo['id'],
            'Resistencia (MPa)': f"{ensayo['resistencia']:.2f}",
            'Fecha': ensayo['fecha'].strftime('%d/%m/%Y')
        }
        for ensayo in sorted(st.session_state.ensayos, key=lambda x: x['fecha'], reverse=True)
    ])
    
    st.dataframe(df_datos, use_container_width=True)
    
    # Estadísticas básicas
    st.header("📊 Estadísticas")
    
    resistencias = [ensayo['resistencia'] for ensayo in st.session_state.ensayos]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Ensayos", len(st.session_state.ensayos))
    
    with col2:
        promedio = sum(resistencias) / len(resistencias)
        st.metric("Resistencia Promedio", f"{promedio:.2f} MPa")
    
    with col3:
        st.metric("Resistencia Máxima", f"{max(resistencias):.2f} MPa")
    
    with col4:
        st.metric("Resistencia Mínima", f"{min(resistencias):.2f} MPa")
    
    # Opciones para mostrar gráfico
    st.header("📈 Visualización")
    
    mostrar_grafico = st.checkbox("Mostrar Gráfico de Resistencias")
    
    if mostrar_grafico:
        # Gráfico simple con matplotlib
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ids = [ensayo['id'] for ensayo in st.session_state.ensayos]
        resistencias = [ensayo['resistencia'] for ensayo in st.session_state.ensayos]
        
        ax.bar(ids, resistencias, color='skyblue', edgecolor='navy', alpha=0.7)
        ax.set_xlabel('ID del Cilindro')
        ax.set_ylabel('Resistencia (MPa)')
        ax.set_title('Resistencia por Cilindro de Concreto')
        ax.grid(True, alpha=0.3)
        
        # Rotar etiquetas del eje x si hay muchos datos
        if len(ids) > 5:
            plt.xticks(rotation=45)
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # Gráfico de histograma
        if len(resistencias) > 3:
            fig2, ax2 = plt.subplots(figsize=(8, 5))
            ax2.hist(resistencias, bins=min(10, len(resistencias)//2 + 1), 
                    color='lightgreen', edgecolor='darkgreen', alpha=0.7)
            ax2.set_xlabel('Resistencia (MPa)')
            ax2.set_ylabel('Frecuencia')
            ax2.set_title('Distribución de Resistencias')
            ax2.grid(True, alpha=0.3)
            
            plt.tight_layout()
            st.pyplot(fig2)
    
    # Opciones adicionales
    st.header("⚙ Opciones")
    
    col_opt1, col_opt2 = st.columns(2)
    
    with col_opt1:
        if st.button("🗑 Limpiar Todos los Datos"):
            st.session_state.ensayos = []
            st.rerun()
    
    with col_opt2:
        # Preparar datos para descarga
        if st.button("📥 Preparar Descarga CSV"):
            csv_data = "ID_Cilindro,Resistencia_MPa,Fecha_Ensayo\n"
            for ensayo in st.session_state.ensayos:
                csv_data += f"{ensayo['id']},{ensayo['resistencia']},{ensayo['fecha']}\n"
            
            st.download_button(
                label="⬇ Descargar CSV",
                data=csv_data,
                file_name=f"ensayos_concreto_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    # Filtro simple
    st.header("🔍 Filtros")
    
    if len(resistencias) > 1:
        min_res = min(resistencias)
        max_res = max(resistencias)
        
        rango = st.slider(
            "Filtrar por rango de resistencia (MPa):",
            min_value=min_res,
            max_value=max_res,
            value=(min_res, max_res),
            step=0.1
        )
        
        # Mostrar ensayos filtrados
        ensayos_filtrados = [
            ensayo for ensayo in st.session_state.ensayos 
            if rango[0] <= ensayo['resistencia'] <= rango[1]
        ]
        
        if len(ensayos_filtrados) != len(st.session_state.ensayos):
            st.write(f"*Mostrando {len(ensayos_filtrados)} de {len(st.session_state.ensayos)} ensayos*")
            
            df_filtrado = pd.DataFrame([
                {
                    'ID Cilindro': ensayo['id'],
                    'Resistencia (MPa)': f"{ensayo['resistencia']:.2f}",
                    'Fecha': ensayo['fecha'].strftime('%d/%m/%Y')
                }
                for ensayo in ensayos_filtrados
            ])
            
            st.dataframe(df_filtrado, use_container_width=True)

else:
    st.info("📝 No hay ensayos registrados. Use el panel lateral para agregar datos.")

# Información del sistema
st.markdown("---")
st.markdown(
    """
    *🔒 Sistema Confidencial - Laboratorio de Materiales*  
    Análisis de ensayos de compresión de cilindros de concreto
    """
)