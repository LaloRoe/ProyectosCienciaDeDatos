import streamlit as st 
import pandas as pd 
import altair as alt

# Código que contenga las instrucciones para el despliegue de un título y una breve descripción de la aplicación web.
st.set_page_config(page_title="Análisis de desempeño de los colaboradores", layout="wide")
st.title("Análisis de desempeño de los colaboradores")
st.markdown("Dashboard para la visualización del desempeño de los colaboradores del área de *Marketing de Socialize your knowledge*")


## Importamos el DataFrame
data = pd.read_csv("Employee_data.csv")

## Limpieza de datos
### Limpiamos espacios vacios como "M ", " M" , etc
data["gender"] = data["gender"].str.strip() 
### Las horas estan multiplicadas por 100, las dividimos para obtener el valor real
data["average_work_hours"] = data["average_work_hours"]/100 


# Código que permita desplegar el logotipo de la empresa en la aplicación web.
st.logo("Img/logo.webp")

############################### SIDEBAR ###############################
st.sidebar.markdown("Selecciona los parámetros que deseas visualizar.")

with st.sidebar:
    #	Código que permita desplegar un control para seleccionar el género del empleado.
    ## Se establecen los valores por defecto como ambos géneros, para que al incio se muestre la información de ambos.
    genero = st.multiselect("Género: ", data["gender"].unique(), default=data["gender"].unique())        

    #	Código que permita desplegar un control para seleccionar un rango del puntaje de desempeño del empleado.
    puntaje = st.slider("Rango de puntaje de desempeño del empleado: ",
    0.0, 
    5.0, 
    (0.0, 5.0)
    )

    #	Código que permita desplegar un control para seleccionar el estado civil del empleado.
    ## Se establece por defecto todos los estados civiles, para que al inicio se muestren todos.
    estado_civil = st.multiselect("Estado civil: ", data["marital_status"].unique(), default=data["marital_status"].unique())

## Máscara lógica para el filtrado de datos con los controles de la sidebar
mask =( (data["gender"].isin(genero)) & 
        (data["performance_score"] >= puntaje[0]) & 
        (data["performance_score"] <= puntaje[1]) & 
        (data["marital_status"].isin(estado_civil))
        )
## DataFrame filtrado con los parámetros que seleccione el usuario en el sidebar
data_filtrada = data[mask]

############################### GRÁFICAS ###############################
## Dividimos el dashboard en dos columnas, como son cuatro gráficas va a quedar una cuadrícula de 4 gráficas
colum1, colum2 = st.columns(2)
## Establezco colores personalizados para cada gráfica ya que el color por defecto no me parecio adecuado.

# Parámetros de las gráficas
ALTURA_GRAFICAS = 210
employee_num = len(data)

#	Código que permita mostrar un gráfico en donde se visualice la distribución de los puntajes de desempeño.
with colum1:
    st.markdown("### Distribución de los puntajes de desempeño")
    ## Considero importante que el usuario pueda visualizar los porcentajes de empleados que representan cada puntaje
    ## Para eso calculamos el porcentaje para mostrarlo en la gráfica
    porcentaje = data_filtrada.groupby('performance_score').size().reset_index(name="conteo")
    porcentaje['conteo'] = porcentaje['conteo']/porcentaje['conteo'].sum()*100


    grafica = alt.Chart(porcentaje).mark_bar().encode(
        x=alt.X("conteo", stack="normalize", title="Proporción de empleados (%)", axis=alt.Axis(format="%")),
        color=alt.Color("performance_score:N", title="Puntaje de desempeño",
                        scale=alt.Scale(range=["#ff4b4b", "#4b8bff", "#4bcc6b", "#ffaa2b"])),
        tooltip=[
            alt.Tooltip("performance_score:N", title="Puntaje"),
            alt.Tooltip("conteo:Q" , title="Porcentaje")
        ]
    ).properties(height=ALTURA_GRAFICAS)

    etiquetas = alt.Chart(porcentaje).mark_text(color="white", fontSize=12, fontWeight="bold").encode(
        x=alt.X("conteo:Q", stack="normalize", bandPosition=0.5),
        text=alt.Text("conteo:Q", format=".1f"),
        order=alt.Order("performance_score:N")
    )
    
    st.altair_chart(grafica + etiquetas, use_container_width=True)

#	Código que permita mostrar un gráfico en donde se visualice la edad de los empleados con respecto al salario de los mismo.
with colum2:
    st.markdown("### Edad de los empleados con respecto al salario de los mismo")
    grafica_edad = alt.Chart(data_filtrada).mark_point(filled = True).encode(
        x = alt.X("salary:Q",scale=alt.Scale(zero=False)),
        y = alt.Y("age:Q",scale=alt.Scale(zero=False)),
        tooltip=[
        alt.Tooltip("age:Q", title="Edad"),
        alt.Tooltip("salary:Q", title="Salario")
    ]    
    ).properties(height=ALTURA_GRAFICAS)
    st.altair_chart(grafica_edad,use_container_width=True)


#	Código que permita mostrar un gráfico en donde se visualice el promedio de horas trabajadas por el género del empleado.
with colum2:
    data_sin_nan = data_filtrada.dropna(subset = ["gender"])
    colores = alt.Scale(domain = data_sin_nan["gender"].unique(), range = ["orange", "green"])
    st.markdown("### Promedio de horas trabajadas por género")

    grafica_genero = alt.Chart(data_sin_nan).mark_bar(filled = True).encode(
        x = alt.X("gender:N"),
        y = alt.Y("mean(average_work_hours):Q"),
        color = alt.Color("gender:N", scale = colores,title="Géneros"),
        tooltip=[
            alt.Tooltip("gender:N", title="Género"),
            alt.Tooltip("mean(average_work_hours):Q", title="Promedio de horas trabajadas")
    ]    
    ).properties(height=ALTURA_GRAFICAS)
    st.altair_chart(grafica_genero,use_container_width=True)


#	Código que permita mostrar un gráfico en donde se visualice la relación del promedio de horas trabajadas versus el puntaje de desempeño.
with colum1:
    data_sin_nan = data_filtrada.dropna(subset = ["performance_score"])
    colores = alt.Scale(domain = data_sin_nan["performance_score"].unique(), range = ["orange", "green","blue","red"])
    st.markdown("### Promedio de horas trabajadas por puntaje de desempeño")

    grafica_genero = alt.Chart(data_sin_nan).mark_bar(filled = True).encode(
        x = alt.X("performance_score:N", title = "Puntaje de desempeño"),
        y = alt.Y("mean(average_work_hours):Q", title = "Promedio de horas trabajadas"),
        color = alt.Color("performance_score:N", scale = colores,title="Puntaje de desempeño")
    ).properties(height=ALTURA_GRAFICAS)
    st.altair_chart(grafica_genero,use_container_width=True)


#	Código que permita desplegar una conclusión sobre el análisis mostrado en la aplicación web.
'''
# Conclusión
* A partir del análisis realizado, se puede observar que no existe una correlación directa 
entre el promedio de horas trabajadas y el puntaje de desempeño de los colaboradores. 
* Se observa que el porcentaje de colaboradores con un puntaje de desempeño de **3** es mucho mayor al resto con un $78.1$%
* En cuanto al promedio de horas trabajadas por desempeño, los de puntaje **1** trabajan $41.6$ hroas en promedio (casi tres horas menos que el resto)
* Además, la distribución salarial muestra variaciones significativas entre distintos rangos 
de edad. 
* En cuanto al género, las horas trabajadas promedio son similares entre hombres y 
mujeres, lo que sugiere equidad en la carga laboral. 
Estos hallazgos pueden servir como base para la toma de decisiones en el área de Marketing de Socialize your knowledge.
'''