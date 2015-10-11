
Client Side
===========


WoW.js
======

Use via settings on Widget Details.

FitText
=======

.. code-block:: html
 
	<span data-fittext>My FitText</span>
	
	<span data-fittext data-fittext=".315" data-fittext-min="12" data-fittext-max="50">My FitText</span>

`NgFitText http://patrickmarabeas.github.io/ng-FitText.js/`_

Multi level dropdown menu
=========================

.. code-block:: html

    <ul class="dropdown-menu multi-level" role="menu" aria-labelledby="dropdownMenu">
        <li><a href="#">Some action</a></li>
        <li><a href="#">Some other action</a></li>
        <li class="dropdown-submenu">
            <a tabindex="-1" href="#">Hover me for more options</a>
            <ul class="dropdown-menu">
                <li><a tabindex="-1" href="#">Second level</a></li>
                <li class="dropdown-submenu">
                    <a href="#">Even More..</a>
                    <ul class="dropdown-menu">
                        <li><a href="#">3rd level</a></li>
                        <li><a href="#">3rd level</a></li>
                    </ul>
                </li>
                <li><a href="#">Second level</a></li>
                <li><a href="#">Second level</a></li>
            </ul>
        </li>
    </ul>
