# Python

!!! info "NOTE:"
    The source code of this example is available in the [Playground](../playground.md). 

Create the following Python script:

<div editor-title="usage/python/hello.py"> 

```python
if __name__ == '__main__':
    print("Hello, world!")
```

</div>

Then, create a workflow YAML file:

<div editor-title=".dstack/workflows/python.yaml">

```yaml
workflows:
  - name: hello-py
    provider: bash
    commands:
      - python usage/python/hello.py
```

</div>

Now, run it locally using the `dstack run` command:

<div class="termy">

```shell
$ dstack run hello-py

RUN           WORKFLOW  SUBMITTED  STATUS     TAG  BACKEND 
shady-1       hello-py  now        Submitted       local
 
Provisioning... It may take up to a minute. ✓

To interrupt, press Ctrl+C.

Hello, world
```

</div>

## Python packages

You can use `pip` within workflows install Python packages.

Let's create the following Python script:

<div editor-title="usage/python/hello_pandas.py"> 

```python
import pandas as pd

if __name__ == '__main__':
    df = pd.DataFrame(
        {
            "Name": [
                "Braund, Mr. Owen Harris",
                "Allen, Mr. William Henry",
                "Bonnell, Miss. Elizabeth",
            ],
            "Age": [22, 35, 58],
            "Sex": ["male", "male", "female"],
        }
    )

    print(df)

```

</div>

Now, create the following workflow YAML file:

<div editor-title=".dstack/workflows/python.yaml"> 

```yaml
workflows:
  - name: hello-pandas
    provider: bash
    commands:
      - pip install pandas
      - python usage/python/hello_pandas.py
```

</div>

Run it locally using the `dstack run` command:

<div class="termy">

```shell
$ dstack run hello-pandas
```

</div>

## Python version

By default, the workflow uses the same Python version that you use locally. 
You can override the major Python version using the `python` property:

<div editor-title=".dstack/workflows/python-version.yaml">

```yaml
workflows:
  - name: python-version
    provider: bash
    python: 3.7
    commands:
      - python --version
```

</div>

Run it locally using the `dstack run` command:

<div class="termy">

```shell
$ dstack run python-version
```

</div>