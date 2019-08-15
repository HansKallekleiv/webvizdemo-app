# Introducing Webviz
---
Webviz is an open source (LGPL-3) web visualization tool being developed by Equinor and built upon [Dash by Plotly](https://plot.ly/products/dash/).

Our aim with Webviz is to empower scientists to share their results easily without the use of proprietary software or complex IT solutions.

Currently our main focus is functionality for result analysis of Equinor's Fast Model Update workflow.

The Webviz framework can however be used in any domain.

<br/>
## Where can I find an example?

This whole page is a Webviz instance. See the `How was this made` section for the underlying configuration file.

<br/>
## User-driven development

Webviz is meant to be customized and extended by users.

Whether you want to visualize a simple graph or a complex machine learning dashboard, as long as it is made with Plotly Dash it should be easy to plug it into Webviz and share it with others.

The [contribution guide](https://github.com/equinor/webviz-config/blob/master/CONTRIBUTING.md) has more details for creating custom elements.

<br/>
## How Webviz works

*The workflow can be summarized as this:*

1) The user provides a configuration file following the [yaml](https://en.wikipedia.org/wiki/YAML) standard.

2) A utility reads the configuration file and automatically writes the corresponding Webviz Dash code.

3) The created application can either be viewed locally, or deployed to a cloud provider. Both out of the box.

Here's a quick demo of a Webviz application being built.

The configuration file is being edited to the left, and the Webviz app is updating live in a web browser to the right.

Note that this example user another `theme` than this page.

![width=100%,height=500px](./demo.gif "Some caption")

To learn more and get started have a look at the [Webviz-config documentation](https://github.com/equinor/webviz-config/blob/master/README.md)

<br/>
## What about security?

[Security evalution of this page](https://observatory.mozilla.org/analyze/webvizvolve.azurewebsites.net)

When hosted, Webviz is run completely sand-boxed with no connections to external databases or file systems.

Additionally we enforce a strict CSP that disallows in-line javascript or linking to external resources.


<br/><br/>





