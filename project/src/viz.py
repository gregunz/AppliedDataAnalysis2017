def world_map_figure(title,
                     title_colorscale,
                     frames_title,
                     df,
                     locations_col,
                     txt_fn,
                     zmin,
                     zmax,
                     colorscale,
                     showscale=True):
    figure = {
        'data': world_map_data(title_colorscale, zmin, zmax, colorscale, showscale),
        'layout': world_map_layout(title, frames_title),
        'frames': world_map_frames(frames_title, df, locations_col, txt_fn)
    }
    return figure


def world_map_layout(title, frames_title):
    sliders_dict = {
        'active': 0,
        'yanchor': 'top',
        'xanchor': 'left',
        'currentvalue': {
            'font': {'size': 20},
            'prefix': '',
            'visible': True,
            'xanchor': 'right'
        },
        'transition': {'duration': 300, 'easing': 'cubic-in-out'},
        'pad': {'b': 10, 't': 50},
        'len': 0.9,
        'x': 0.1,
        'y': 0,
        'steps': []
    }

    for name in frames_title:
        slider_step = {'args': [
            [name],
            {'frame': {
                'duration': 300,
                'redraw': False
            },
                'mode': 'immediate',
                'transition': {'duration': 300}
            }
        ],
            'label': name,
            'method': 'animate'
        }
        sliders_dict['steps'].append(slider_step)

    layout = {
        'title': title,
        'width': 1080,
        'height': 720,
        'geo': {
            'showframe': True,
            'showcoastlines': False,
            'showland': True,
            'landcolor': 'gray',
            'projection': {
                'type': 'Mercator'
            },
            'bgcolor': 'rgba(0, 0, 0, 0)',
        },
        'sliders': [sliders_dict],
        'updatemenus': [{
            'buttons': [
                {
                    'args': [None, {'frame': {'duration': 500, 'redraw': False},
                                    'fromcurrent': True,
                                    'transition': {'duration': 300, 'easing': 'quadratic-in-out'}}],
                    'label': 'Play',
                    'method': 'animate'
                },
                {
                    'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate',
                                      'transition': {'duration': 0}}],
                    'label': 'Pause',
                    'method': 'animate'
                }
            ],
            'direction': 'left',
            'pad': {'r': 10, 't': 87},
            'showactive': False,
            'type': 'buttons',
            'x': 0.1,
            'xanchor': 'right',
            'y': 0,
            'yanchor': 'top',
        }],
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    }

    return layout


def world_map_data(title_colorscale, zmin, zmax, colorscale, showscale=True):
    data = [{
        'type': 'choropleth',
        'zmin': zmin,
        'zmax': zmax,
        'showscale': showscale,
        'colorscale': colorscale,
        'reversescale': False,
        'marker': {
            'line': {
                'color': 'rgb(180,180,180)',
                'width': 0.5
            }
        },
        'colorbar': {
            'title': title_colorscale
        },
    }]
    return data


def world_map_frames(frames_title, df, locations_col, txt_fn):
    frames = []
    for name in frames_title:
        frame_data = {
            'locations': df[locations_col],
            'z': df[name],
            'text': df[locations_col].apply(txt_fn),
        }
        frame = {
            'data': [frame_data],
            'name': name,
        }
        frames.append(frame)
    return frames
