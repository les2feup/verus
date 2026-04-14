Installation
============

VERUS can be installed using pip:

.. code-block:: bash

    pip install verus

Development Installation
------------------------

For development, clone the repository and install in development mode:

.. code-block:: bash

    git clone https://github.com/les2feup/verus.git
    cd verus
    pip install -e .

Dependencies
------------

VERUS requires the following key dependencies:

- Python 3.8+
- NumPy
- Pandas
- GeoPandas
- Scikit-learn
- OSMnx
- Folium
- Haversine
- H3 (``h3>=4.0.0``) — required for H3-based hexagonal grid generation

These dependencies will be automatically installed when installing VERUS with pip.

H3 Library Notes
^^^^^^^^^^^^^^^^

The ``h3`` package includes pre-built wheels for the most common platforms
(Linux x86-64, macOS, Windows). On less common architectures it may fall
back to compiling the underlying C library. If that happens, install the
build tools first:

**Debian / Ubuntu**

.. code-block:: bash

    sudo apt install cmake make gcc libtool

**Alpine**

.. code-block:: bash

    apk add cmake make gcc libtool musl-dev

**macOS**

.. code-block:: bash

    brew install cmake
    # or install the full H3 C library and CLI tools:
    brew install h3