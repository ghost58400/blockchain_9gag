<?php
  class DBConnect {
    private static $instance=NULL;

    public static function getInstance(){
      $opt = array(
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            PDO::ATTR_EMULATE_PREPARES => FALSE,
        );

      if (!isset(self::$instance)) {

         self::$instance= new PDO("mysql:host=localhost;dbname=taskdb","root","orange",$opt);
      } // end if
      return self::$instance;
    }//end getInstance

  }//end class


?>
