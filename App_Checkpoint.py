import streamlit as st
import SimpleITK as sitk
import tempfile
import os
import textwrap
from PIL import Image

#### Funciones propias #### 
from RotarVolumen import leer_archivos_dicom, leer_archivos_dicom_mult, process_dicom,process_dicom_mult
from inferencia import CargarVolumen_YOLO, uso_RUBEN, uso_RUBEN_mult, uso_YOLO, uso_YOLO_mult
from conversor import carpetaPNG, carpetaDCM, descargaPNG

#### Estilo HTML ####

#### Tarjeta #### 
st.markdown('''
        <style>
        .card {
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 12px;
            border: 1px solid #ddd;
            margin-top: 10px;
        }
        .card h4 {
            margin-top: 0;
        }
        </style>
        ''', unsafe_allow_html=True)

#### Botones #### 
st.markdown('''
        <style>
        .stDownloadButton button {
            background-color: #E66717;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            border: none;
        }
        .stDownloadButton button:hover {
            background-color: #D46924;
        }
            </style>
        ''', unsafe_allow_html=True)


#### Inicializar #### 
if 'screen' not in st.session_state:
    st.session_state.screen = 1

def go_welcome():
    st.session_state.screen = 1

def go_lobby():
    st.session_state.screen = 2

#### Presentacion #### 
if st.session_state.screen == 1:
    st.title('Welcome')
    st.markdown('Press **Start** to enter')
    st.button('Start ▶️', on_click = go_lobby)
	
#### Lobby #### 
elif st.session_state.screen == 2:

    st.set_page_config(layout='wide')
	
    upload_dcm_1 = st.sidebar.file_uploader('**Archivos DCM 1**', type=['DCM'],
                                            accept_multiple_files=True, key='dcm1')
    
    upload_dcm_2 = st.sidebar.file_uploader('**Archivos DCM 2**', type=['DCM'],
                                            accept_multiple_files=True, key='dcm2')

    upload_dcm_3 = st.sidebar.file_uploader('**Archivos DCM 3**', type=['DCM'],
                                            accept_multiple_files=True, key='dcm3')

    upload_dcm_4 = st.sidebar.file_uploader('**Archivos DCM 4**', type=['DCM'],
                                            accept_multiple_files=True, key='dcm4')

    upload_dcm_5 = st.sidebar.file_uploader('**Archivos DCM 5**', type=['DCM'],
                                            accept_multiple_files=True, key='dcm5')

    upload_dcm_6 = st.sidebar.file_uploader('**Archivos DCM 6**', type=['DCM'],
                                            accept_multiple_files=True, key='dcm6')
    
    upload_dcm_7 = st.sidebar.file_uploader('**Archivos DCM 7**', type=['DCM'],
                                            accept_multiple_files=True, key='dcm7')

    upload_dcm_8 = st.sidebar.file_uploader('**Archivos DCM 8**', type=['DCM'],
                                            accept_multiple_files=True, key='dcm8')

    upload_dcm_9 = st.sidebar.file_uploader('**Archivos DCM 9**', type=['DCM'],
                                            accept_multiple_files=True, key='dcm9')

    upload_dcm_10 = st.sidebar.file_uploader('**Archivos DCM 10**', type=['DCM'],
                                            accept_multiple_files=True, key='dcm10')

    upload_dcm_11 = st.sidebar.file_uploader('**Archivos DCM 11**', type=['DCM'],
                                            accept_multiple_files=True, key='dcm11')
    
    if upload_dcm_1:
        
        upload_dcms = [upload_dcm_1,upload_dcm_2,upload_dcm_3,upload_dcm_4,upload_dcm_5,
                       upload_dcm_6,upload_dcm_7,upload_dcm_8,upload_dcm_9,upload_dcm_10,
                       upload_dcm_11]
        
        st.write(len(upload_dcms))
        # ------------------------------------------------------------------------------------
        #                                   SUBIDA DE DATOS
        # ------------------------------------------------------------------------------------
		#### Carpeta temporal DICOM ####
        if 'rutas_DCM' not in st.session_state:
            rutas_DCM = []

            for upload_dcm in upload_dcms:
                temp_dcm_org = tempfile.mkdtemp()
                
                for f in upload_dcm:
                    path = os.path.join(temp_dcm_org, f.name)
                    with open(path, 'wb') as out:
                        out.write(f.getbuffer())

                rutas_DCM.append(temp_dcm_org)

            st.session_state.rutas_DCM = rutas_DCM

        rutas_DCM = st.session_state.rutas_DCM

        # ------------------------------------------------------------------------------------
        #                                      ORIGINAL
        # ------------------------------------------------------------------------------------

        #### Volumenes ####
        if 'HV_org' not in st.session_state:
            st.session_state.HV_org = leer_archivos_dicom_mult(rutas_DCM)

        HV_org = st.session_state.HV_org

		#### Carpetas temporal PNG ####
        if 'temp_png_orgs' not in st.session_state:
            
            st.session_state.temp_png_orgs = [carpetaPNG(V_org,0) for V_org in HV_org]

        temp_png_orgs = st.session_state.temp_png_orgs

        # ------------------------------------------------------------------------------------
        #                                   ESTÁNDAR
        # ------------------------------------------------------------------------------------
        #### Inferencia de los parámetros ####
        if 'p_std' not in st.session_state: 
            st.session_state.p_std = uso_RUBEN_mult('mvit_v2_s_estandar.pt',
                                                    temp_png_orgs)
        
        p_std = st.session_state.p_std

    	#### Rotación ####
        if 'HV_std' not in st.session_state:
            HV_std, spcs_std = process_dicom_mult(p_std,rutas_DCM)

            st.session_state.HV_std = HV_std
            st.session_state.spcs_std = spcs_std

        spcs_std = st.session_state.spcs_std
        HV_std = st.session_state.HV_std
		
		#### Carpeta temporal DICOM ####
        if 'temp_dcm_stds' not in st.session_state:		

            st.session_state.temp_dcm_stds = [carpetaDCM(HV_std[i], spcs_std [i]) for i in range(len(HV_std))]

        temp_dcm_stds = st.session_state.temp_dcm_stds
        
		#### Carpeta temporal PNG ####
        if 'temp_png_stds' not in st.session_state:
            
            st.session_state.temp_png_stds  = [carpetaPNG(V_std,0) for V_std in HV_std]
            
        temp_png_stds = st.session_state.temp_png_stds

        # ------------------------------------------------------------------------------------
        #                                         LVOT
        # ------------------------------------------------------------------------------------
        #### Inferencia de los parámetros ####
        if 'p_LVOT' not in st.session_state: 
            st.session_state.p_LVOT = uso_RUBEN_mult('mvit_v2_s_lvot.pt',
                                                    temp_png_stds)
        
        p_LVOT = st.session_state.p_LVOT

    	#### Rotación ####
        if 'HV_LVOT' not in st.session_state:
            HV_LVOT, _ = process_dicom_mult(p_LVOT,temp_dcm_stds)

            st.session_state.HV_LVOT = HV_LVOT

        HV_LVOT = st.session_state.HV_LVOT

		#### Carpeta temporal PNG ####
        if 'temp_png_LVOTs' not in st.session_state:
            
            st.session_state.temp_png_LVOTs  = [carpetaPNG(V_LVOT,0) for V_LVOT in HV_LVOT]
            
        temp_png_LVOTs = st.session_state.temp_png_LVOTs

        # ------------------------------------------------------------------------------------
        #                                   VALVULA
        # ------------------------------------------------------------------------------------
        #### Carpeta temporal PNG ####
        if 'temp_png_valvs' not in st.session_state:

            HV_valv = [[V_LVOT[:,i,:] for i in range(V_LVOT.shape[2])] for V_LVOT in HV_LVOT]
            st.session_state.temp_png_valvs = [carpetaPNG(V_valv,0) for V_valv in HV_valv]

        temp_png_valvs = st.session_state.temp_png_valvs
        
        # ------------------------------------------------------------------------------------
        #                                    YOLO
        # ------------------------------------------------------------------------------------
        if 'temp_png_YOLOs' not in st.session_state:
            HV_YOLO = [CargarVolumen_YOLO(ruta) for ruta in temp_png_valvs]
            st.session_state.temp_png_YOLOs  = [carpetaPNG(V_YOLO[:,:,:,0],0) for V_YOLO in HV_YOLO]

        temp_png_YOLOs = st.session_state.temp_png_YOLOs

        # ------------------------------------------------------------------------------------
        #                                   DETECCIÓN
        # ------------------------------------------------------------------------------------
        if 'temp_png_RGB' not in st.session_state:
            HV_RGB, HV_masks, Indcs  = uso_YOLO_mult('best.pt',temp_png_YOLOs)

            st.session_state.temp_png_RGB = [carpetaPNG(V_RGB,1) for V_RGB in HV_RGB]
            st.session_state.temp_png_masks = [carpetaPNG(V_masks[:,:,:],0) for V_masks in HV_masks]
            st.session_state.numb_sld = (HV_RGB[0].shape[0], Indcs[0][0], Indcs[0][1])
            st.session_state.INDICES = Indcs
            st.session_state.HV_RGB = HV_RGB


        numb_sld = st.session_state.numb_sld
        temp_png_RGB = st.session_state.temp_png_RGB
        temp_png_masks = st.session_state.temp_png_masks
        Indcs = st.session_state.INDICES
        HV_RGB = st.session_state.HV_RGB
        
        # ------------------------------------------------------------------------------------
        #                                  Descargar PNG'S 
        # ------------------------------------------------------------------------------------      
#        des1, des2, des3 = st.columns(3)
#        
#        with des1:
#            zip_data = descargaPNG(temp_png_org)
#            st.download_button(
#                label='Descargar PNG originales',
#                data=zip_data,
#                file_name='PNG_ORIGINALES.zip',
#                mime='application/zip'
#            )
#        
#        with des2:
#            zip_data = descargaPNG(temp_png_std)
#            st.download_button(
#                label='Descargar PNG estandar',
#                data=zip_data,
#                file_name='PNG_ESTANDAR.zip',
#                mime='application/zip'
#            )
#        
#        with des3:
#            zip_data = descargaPNG(temp_png_LVOT)
#            st.download_button(
#                label='Descargar PNG LVOT',
#                data=zip_data,
#                file_name='PNG_LVOT.zip',
#                mime='application/zip'
#            )

        # ------------------------------------------------------------------------------------
        #                                  Descargar PNG'S 
        # ------------------------------------------------------------------------------------      
#       des1, des2, des3 = st.columns(3)
#        
#        with des1:
#            zip_data = descargaPNG(temp_png_YOLOs[0])
#            st.download_button(
#                label='Descargar 1',
#                data=zip_data,
#                file_name='1.zip',
#                mime='application/zip')
#        
#        with des2:
#            zip_data = descargaPNG(temp_png_YOLOs[1])
#            st.download_button(
#                label='Descargar 2',
#                data=zip_data,
#                file_name='2.zip',
#                mime='application/zip')
#        
#        with des3:
#            zip_data = descargaPNG(temp_png_YOLOs[2])
#            st.download_button(
#                label='Descargar 2',
#                data=zip_data,
#                file_name='3.zip',
#                mime='application/zip')

		#### Pestañas ####
        tab1, tab2, tab3 = st.tabs(['Estándar', 'LVOT', 'Mascara'])

        # ------------------------------------------------------------------------------------
        #                                 Pestaña Estandar
        # ------------------------------------------------------------------------------------   
        with tab1:    	
			
            html_1 = f'''
                <div class="card">
                    <h4>Parametros</h4>
                    <b>Ángulo:</b> {p_std[0][0]:.4f} <br>
                    <b>Vector:</b> [{p_std[0][1]:.6f}, {p_std[0][2]:.6f}, {p_std[0][3]:.6f}]
                </div>
            '''
            st.markdown(textwrap.dedent(html_1), unsafe_allow_html=True)

            html_3 = f'''
                <div class="card">
                    <h4>Imagenes</h4>
                </div>
            '''
            st.markdown(textwrap.dedent(html_3), unsafe_allow_html=True)

            N_std_2 = st.slider('Volumen',min_value=1, max_value=len(HV_org), step=1,key ='sld_std_2')
            N_std_1 = st.slider('Corte',min_value=1, max_value=HV_org[0].shape[0], step=1,key ='sld_std_1')
    
            img_orig_user_1 = Image.open(os.path.join(temp_png_orgs[N_std_2-1], f'slice_{(N_std_1-1):03d}.png'))
            img_fnl_user_1 = Image.open(os.path.join(temp_png_stds[N_std_2-1], f'slice_{(N_std_1-1):03d}.png'))
          
            col1, col2 = st.columns(2)
            with col1:
                st.image(img_orig_user_1, caption='Original', use_container_width=True)
            with col2:
                st.image(img_fnl_user_1, caption='Estandar', use_container_width=True)
		
        # ------------------------------------------------------------------------------------
        #                                 Pestaña LVOT
        # ------------------------------------------------------------------------------------
        with tab2:
          
            html_1 = f'''
                <div class="card">
                    <h4>Parametros</h4>
                    <b>Ángulo:</b> {p_LVOT[0][0]:.4f} <br>
                    <b>Vector:</b> [{p_LVOT[0][1]:.6f}, {p_LVOT[0][2]:.6f}, {p_LVOT[0][3]:.6f}]
                </div>
            '''
            st.markdown(textwrap.dedent(html_1), unsafe_allow_html=True)
 
            html_3 = f'''
                <div class="card">
                    <h4>Imagenes</h4>
                </div>
            '''
            st.markdown(textwrap.dedent(html_3), unsafe_allow_html=True)

            N_LVOT_1 = st.slider('Volumen', min_value=1, max_value = len(HV_org), step=1, key ='sld_LVOT_1')
            N_LVOT_2 = st.slider('Corte', min_value=1, max_value = HV_org[0].shape[0], step=1, key ='sld_LVOT_2')
    
            img_orig_user_2 = Image.open(os.path.join(temp_png_stds[N_LVOT_1-1], f'slice_{(N_LVOT_2-1):03d}.png'))
            img_fnl_user_2 = Image.open(os.path.join(temp_png_LVOTs[N_LVOT_1-1], f'slice_{(N_LVOT_2-1):03d}.png'))
          
            col1, col2 = st.columns(2)
            with col1:
                st.image(img_orig_user_2, caption='Estandar', use_container_width=True)
            with col2:
                st.image(img_fnl_user_2, caption='LVOT', use_container_width=True)
    
        # ------------------------------------------------------------------------------------
        #                                 Pestaña Deteccion
        # ------------------------------------------------------------------------------------
        with tab3:

            html_3 = f'''
                <div class="card">
                    <h4>Valvula</h4>
                </div>
            '''
            st.markdown(textwrap.dedent(html_3), unsafe_allow_html=True)

            N_valva_1 = st.slider('',min_value=1, max_value=len(HV_org), step=1, key = 'sld_valva_1')
            N_valva_2 = st.slider('',min_value=1, max_value=HV_org[0].shape[1], step=1, key = 'sld_valva_2')

            img_orig_user_valva = Image.open(os.path.join(temp_png_YOLOs[N_valva_1-1], f'slice_{(N_valva_2-1):03d}.png'))

            valv1, valv2, valv3 = st.columns([1,2,1])
            with valv1:
                st.write('')

            with valv2:
                st.image(img_orig_user_valva, caption=' ', use_container_width=True)

            with valv3:
                st.write('')

            html_3 = f'''
                <div class="card">
                    <h4>Deteccion</h4>
                </div>
            '''
            st.markdown(textwrap.dedent(html_3), unsafe_allow_html=True)
                            
            N_mask_1 = st.slider(' ',min_value=1, max_value=len(HV_org), step=1, key = 'sld_mask_1')
            N_mask_2 = st.slider(' ',min_value=1, max_value=HV_RGB[N_mask_1-1].shape[0], step=1, key = 'sld_mask_2')
            
            xmin, xmax, z, u = 0, HV_RGB[N_mask_1-1].shape[0], Indcs[N_mask_1-1][0], Indcs[N_mask_1-1][1]+1 
            
            width = 100
            start = (z-xmin)/(xmax-xmin)*100
            end = (u-xmin)/(xmax-xmin)*100
            
            st.markdown(f'''
            <div style='width:100%; height:10px; background-color:rgb(89,193,201); position:relative;'>
                <div style='
                    position:absolute;
                    left:{start}%;
                    width:{end-start}%;
                    height:100%;
                    background-color:rgb(47,79,247);'>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)

            simb1, simb2, simb3 = st.columns(3)

            with simb1:
                st.markdown(
                    '''
                    <div style='display:flex; align-items:center;'>
                        <div style='width:20px; height:20px; background-color:rgb(190,190,190); 
                        margin-right:10px; border-radius:3px;'></div>
                        <span><b>Sin deteccion</b></span>
                    </div>
                    ''', unsafe_allow_html=True)

            with simb2:
                st.markdown(
                    '''
                    <div style='display:flex; align-items:center;'>
                        <div style='width:20px; height:20px; background-color:rgb(89,193,201); 
                        margin-right:10px; border-radius:3px;'></div>
                        <span><b>Tracto</b></span>
                    </div>
                    ''', unsafe_allow_html=True)

            with simb3:
                st.markdown(
                    '''
                    <div style='display:flex; align-items:center;'>
                        <div style='width:20px; height:20px; background-color:rgb(59,75,247); 
                        margin-right:10px; border-radius:3px;'></div>
                        <span><b>Valvula aortica</b></span>
                    </div>
                    ''', unsafe_allow_html=True)

            img_orig_user_3 = Image.open(os.path.join(temp_png_RGB[N_mask_1-1], f'slice_{(N_mask_2-1):03d}.png'))
            img_fnl_user_3 = Image.open(os.path.join(temp_png_masks[N_mask_1-1], f'slice_{(N_mask_2-1):03d}.png'))

            st.write('')
            col1, col2 = st.columns(2)
            with col1:
                st.image(img_orig_user_3, caption='Deteccion', use_container_width=True)
            with col2:
                st.image(img_fnl_user_3, caption='Mascara', use_container_width=True)