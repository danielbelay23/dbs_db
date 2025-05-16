import streamlit as st
from streamlit_flow import streamlit_flow
from streamlit_flow.elements import StreamlitFlowNode, StreamlitFlowEdge
from streamlit_flow.state import StreamlitFlowState

# svg to png conversion https://www.photopea.com/ 

nodes = [
    StreamlitFlowNode(
        id='.wav,',
        pos=(100, 100),
        data={'content': 'Original Footage'},
        node_type='input',
        source_position='right'
    ),
    
    StreamlitFlowNode(
        id='original_sound',
        pos=(100, 300),
        data={'content': 'Original Sound'},
        node_type='input',
        source_position='right'
    ),
    
    StreamlitFlowNode(
        id='video_codec_1',
        pos=(300, 100),
        data={'content': 'Video Codec'},
        node_type='default',
        source_position='right',
        target_position='left'
    ),
    
    StreamlitFlowNode(
        id='audio_codec_1',
        pos=(300, 300),
        data={'content': 'Audio Codec'},
        node_type='default',
        source_position='right',
        target_position='left'
    ),
    
    StreamlitFlowNode(
        id='encoding_label',
        pos=(300, 200),
        data={'content': 'Encoding'},
        node_type='default'
    ),
    
    StreamlitFlowNode(
        id='container',
        pos=(500, 200),
        data={'content': 'Video File'},
        node_type='default',
        source_position='right',
        target_position='left'
    ),
    
    StreamlitFlowNode(
        id='decoding_label',
        pos=(700, 200),
        data={'content': 'Decoding'},
        node_type='default'
    ),
    
    StreamlitFlowNode(
        id='video_codec_2',
        pos=(700, 100),
        data={'content': 'Video Codec'},
        node_type='default',
        source_position='right',
        target_position='left'
    ),
    
    StreamlitFlowNode(
        id='audio_codec_2',
        pos=(700, 300),
        data={'content': 'Audio Codec'},
        node_type='default',
        source_position='right',
        target_position='left'
    ),
    
    StreamlitFlowNode(
        id='video_footage_label',
        pos=(700, 50),
        data={'content': 'Video Footage'},
        node_type='default'
    ),
    
    StreamlitFlowNode(
        id='sound_label',
        pos=(700, 350),
        data={'content': 'Sound'},
        node_type='default'
    ),
    
    StreamlitFlowNode(
        id='playback',
        pos=(900, 200),
        data={'content': 'Playback'},
        node_type='output',
        target_position='left'
    ),
]

edges = [
    StreamlitFlowEdge(
        id='orig-footage-to-video',
        source='original_footage',
        target='video_codec_1',
        animated=True
    ),
    
    StreamlitFlowEdge(
        id='orig-sound-to-audio',
        source='original_sound',
        target='audio_codec_1',
        animated=True
    ),
    
    StreamlitFlowEdge(
        id='video-codec-to-container',
        source='video_codec_1',
        target='container',
        animated=True
    ),
    
    StreamlitFlowEdge(
        id='audio-codec-to-container',
        source='audio_codec_1',
        target='container',
        animated=True
    ),
    
    StreamlitFlowEdge(
        id='container-to-video-codec',
        source='container',
        target='video_codec_2',
        animated=True
    ),
    
    StreamlitFlowEdge(
        id='container-to-audio-codec',
        source='container',
        target='audio_codec_2',
        animated=True
    ),
    StreamlitFlowEdge(
        id='video-codec-to-playback',
        source='video_codec_2',
        target='playback',
        animated=True
    ),
    StreamlitFlowEdge(
        id='audio-codec-to-playback',
        source='audio_codec_2',
        target='playback',
        animated=True
    ),
]

if 'minimap_controls_state' not in st.session_state:
    st.session_state.minimap_controls_state = StreamlitFlowState(nodes, edges)

# https://discuss.streamlit.io/t/new-component-streamlit-flow-beautiful-interactive-and-flexible-flow-diagrams-in-streamlit/67505
# styling, css limitations 
# https://stflow.streamlit.app/Custom_Styles
# streamlit_flow(
#     'minimap_controls_flow', 
#     st.session_state.minimap_controls_state, 
#     fit_view=True, 
#     show_minimap=True, 
#     show_controls=True,
#     hide_watermark=True
# )

results = streamlit_flow(
    'minimap_controls_flow', 
    st.session_state.minimap_controls_state, 
    fit_view=True, 
    show_minimap=True, 
    show_controls=True,
    hide_watermark=True
)

