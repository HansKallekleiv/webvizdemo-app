#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import logging
import logging.config
import socket
import os.path as path
from pathlib import Path, PosixPath

import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
from flask_talisman import Talisman
from webviz_config.common_cache import cache
from webviz_config.webviz_store import webviz_storage
from webviz_config.webviz_assets import webviz_assets
import webviz_config.containers as standard_containers



logging.getLogger('werkzeug').setLevel(logging.WARNING)

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {'default': {
        'format': ' webviz log [%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        'datefmt': '%Y-%m-%d %H:%M:%S'
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = dash.Dash(__name__, external_stylesheets=['https://webviz-cdn.azureedge.net/fonts/index.css', 'https://webviz-cdn.azureedge.net/theme/equinor.theme.css'])
server = app.server

app.title = 'Introducing Webviz'
app.config.suppress_callback_exceptions = True

app.webviz_settings = {
    'portable': True,
    'plotly_layout': {}
                      }

cache.init_app(server)

CSP = {'default-src': "'none'", 'connect-src': "'self'", 'prefetch-src': "'self'", 'style-src': ["'self'", "'unsafe-inline'", 'https://webviz-cdn.azureedge.net'], 'script-src': ["'self'", "'unsafe-eval'", "'sha256-jZlsGVOhUAIcH+4PVs7QuGZkthRMgvT2n0ilH6/zTM0='"], 'img-src': ["'self'", 'data:', 'https://sibwebvizcdn.blob.core.windows.net'], 'navigate-to': "'self'", 'base-uri': "'self'", 'form-action': "'self'", 'frame-ancestors': "'none'", 'child-src': "'none'", 'object-src': "'self'", 'plugin-types': 'application/pdf', 'font-src': ['https://webviz-cdn.azureedge.net']}
FEATURE_POLICY = {'camera': "'none'", 'geolocation': "'none'", 'microphone': "'none'", 'payment': "'none'"}

Talisman(server, content_security_policy=CSP, feature_policy=FEATURE_POLICY)

webviz_storage.use_storage = True
webviz_storage.storage_folder = path.join(path.dirname(path.realpath(__file__)),
                                          'webviz_storage')

webviz_assets.portable = True


app.layout = dcc.Tabs(parent_className="layoutWrapper",
                      content_className='pageWrapper',
                      vertical=True, children=[
   
    dcc.Tab(id='logo',
            className='styledLogo',children=[
                 standard_containers.Markdown(**{'markdown_file': PosixPath('/tmp/webviz/dev/intersect/demo/demo/introduction.md')}).layout
                 ]
    ),
    dcc.Tab(id='webviz_in_fmu',label='Webviz in FMU',
            selected_className='selectedButton',
            className='styledButton',children=[
                 standard_containers.Markdown(**{'markdown_file': PosixPath('/tmp/webviz/dev/intersect/demo/demo/fmu.md')}).layout,
                 dcc.Markdown(r'''### Understanding uncertainty in model parameters'''),
                 dcc.Markdown(r'''Explore and QC model parameters both as prior (input) distributions and how they are adjusted after being updated by the Ensemble Smoother method.'''),
                 dcc.Markdown(r'''The correlation matrix shows the pairwise correlation of all model parameters. To investigate the distribution of each pair, click a cell or choose manually from the selectors.'''),
                 standard_containers.ParameterDistribution(app=app, **{'ensembles': ['prior', 'posterior'], 'container_settings': {'scratch_ensembles': {'reek': '/scratch/fmu/eza/25_r002_reek/realization-*/iter-0/', 'struct_unc': '/scratch/fmu/hakal/volve/volve_example3/realization-*/iter-0', 'prior': '/scratch/fmu/akia/volve/volve_example2/realization-*/iter-0', 'posterior': '/scratch/fmu/akia/volve/volve_example2/realization-*/iter-3'}}}).layout,
                 dcc.Markdown(r'''---'''),
                 dcc.Markdown(r'''### Uncertainty in simulation profiles'''),
                 dcc.Markdown(r'''Resulting simulation profiles from an ensemble of simulation runs'''),
                 dcc.Markdown(r'''Different vectors can be selected and visualized either per realization or as summarized statistics.'''),
                 standard_containers.SummaryStats(app=app, **{'ensembles': ['prior'], 'container_settings': {'scratch_ensembles': {'reek': '/scratch/fmu/eza/25_r002_reek/realization-*/iter-0/', 'struct_unc': '/scratch/fmu/hakal/volve/volve_example3/realization-*/iter-0', 'prior': '/scratch/fmu/akia/volve/volve_example2/realization-*/iter-0', 'posterior': '/scratch/fmu/akia/volve/volve_example2/realization-*/iter-3'}}}).layout,
                 dcc.Markdown(r'''---'''),
                 dcc.Markdown(r'''### Evaluating production misfit'''),
                 dcc.Markdown(r'''Production misfit of different ensembles with varying degree of seismic conditioning implemented.'''),
                 dcc.Markdown(r'''No conditioning in the left-most plot and increased conditioning towards the right'''),
                 dcc.Markdown(r'''Each point represents one model run (realization)'''),
                 standard_containers.TablePlotter(app=app, **{'csv_file': PosixPath('/tmp/webviz/dev/intersect/demo/demo/misfit.csv'), 'plot_options': {'x': 'prod_misfit', 'y': 'ts3map_misfit', 'facet_col': 'case'}, 'lock': True}).layout,
                 dcc.Markdown(r'''iter-0  --  prior'''),
                 dcc.Markdown(r'''noseis  --  conditioning to prod data, RFT'''),
                 dcc.Markdown(r'''ts1maps --  conditioning to prod data, RFT, 1 4D TS map (2003-2000)'''),
                 dcc.Markdown(r'''ts2map  --  conditioning to prod data, RFT, 2 4D TS maps (2001-200, 2003-2001)'''),
                 dcc.Markdown(r'''ts3map  --  conditioning to prod data, RFT, 3 4D TS maps (2001-2000, 2003-2001, 2003-2000)''')
                 ]
    ),
    dcc.Tab(id='work_in_progress',label='Work in progress',
            selected_className='selectedButton',
            className='styledButton',children=[
                 standard_containers.Markdown(**{'markdown_file': PosixPath('/tmp/webviz/dev/intersect/demo/demo/inprogress.md')}).layout
                 ]
    ),
    dcc.Tab(id='how_was_this_made',label='How was this made',
            selected_className='selectedButton',
            className='styledButton',children=[
                 dcc.Markdown(r'''This **Webviz instance** was created from the following configuration file'''),
                 standard_containers.SyntaxHighlighter(**{'filename': PosixPath('/tmp/webviz/dev/intersect/demo/demo/basic_example.yaml'), 'dark_theme': True}).layout
                 ]
    ),
    dcc.Tab(id='last_page',label='Resources',
            selected_className='selectedButton',
            className='styledButton',children=[
                 standard_containers.Markdown(**{'markdown_file': PosixPath('/tmp/webviz/dev/intersect/demo/demo/resources.md')}).layout
                 ]
    )]
)

if __name__ == '__main__':
    # This part is ignored when the webviz app is started
    # using Docker container and uwsgi (e.g. when hosted on Azure).

    dash_auth.BasicAuth(app, {'some_username': 'some_password'})
    app.run_server(host='localhost', port=8050, ssl_context=('server.crt', 'server.key'), debug=False, use_reloader=True, dev_tools_hot_reload=True, dev_tools_hot_reload_interval=1.0)