<?php
 
// Токен
  const TOKEN = '6232376592:AAGpQ-XyADH43xqpCvAlOtmKGLH2oRcCKXY';
 
  // ID чата
  const CHATID = '-1001921404476';
 

  $types = array('image/gif', 'image/png', 'image/jpeg', 'application/pdf');

  $size = 1073741824; // 1 ГБ
 
if ($_SERVER["REQUEST_METHOD"] == "POST") {
 
  $fileSendStatus = '';
  $textSendStatus = '';
  $msgs = [];
   
  // Проверяем не пусты ли поля 
  if (!empty($_POST['name'] && !empty($_POST['surname'] && !empty($_POST['phone'])))) {
     
    // Если не пустые, то валидируем эти поля и сохраняем и добавляем в тело сообщения. Минимально для теста так:
    $txt = "";
     
    // Имя
    if (isset($_POST['name'])) {
        $txt .= "Имя пославшего: " . strip_tags(trim(urlencode($_POST['name']))) . "%0A";
    }
    if (isset($_POST['surname'])) {
        $txt .= "Фамилия " . strip_tags(trim(urlencode($_POST['surname']))) . "%0A";
    }
    if (isset($_POST['phone'])) {
        $txt .= "Номер телефона: " . strip_tags(trim(urlencode($_POST['phone']))) . "%0A";
    }
    if (isset($_POST['company'])) {
        $txt .= "Компания: " . strip_tags(trim(urlencode($_POST['company']))) . "%0A";
    }
    if (isset($_POST['email'])) {
        $txt .= "Эл.почта: " . strip_tags(trim(urlencode($_POST['email']))) . "%0A";
    }
    
    if (isset($_POST['desk_project'])) {
        $txt .= "Описание проекта: " . strip_tags(trim(urlencode($_POST['desk_project']))) . "%0A";
    }
    if(isset($_POST["site"]))
      {
          $site = $_POST["site"];
          $txt .=  $site . "%0A";
      }
    if(isset($_POST["web-app"]))
      {
          $webApp = $_POST["web-app"];
          $txt .=  $webApp . "%0A";
      }

      if(isset($_POST["mobile-app"]))
      {
          $mobileApp = $_POST["mobile-app"];
          $txt .=  $mobileApp . "%0A";
      }

      if(isset($_POST["design"]))
      {
          $design = $_POST["design"];
          $txt .=  $design . "%0A";
      }

      if(isset($_POST["testing"]))
      {
          $testing = $_POST["testing"];
          $txt .=  $testing . "%0A";
      }


      //Баксы деньги доллоры
      if(isset($_POST["doSto"]))
      {
          $doSto = $_POST["doSto"];
          $txt .=  $doSto . "%0A";
      }


      if(isset($_POST["stoPtos"]))
      {
          $stoPtos = $_POST["stoPtos"];
          $txt .=  $stoPtos . "%0A";
      }

      if(isset($_POST["ptosMil"]))
      {
          $ptosMil = $_POST["ptosMil"];
          $txt .=  $ptosMil . "%0A";
      }

      if(isset($_POST["odinDvaMil"]))
      {
          $odinDvaMil = $_POST["odinDvaMil"];
          $txt .=  $odinDvaMil . "%0A";
      }

      if(isset($_POST["mnogoDeneg"]))
      {
          $mnogoDeneg = $_POST["mnogoDeneg"];
          $txt .=  $mnogoDeneg . "%0A";
      }

 
    $textSendStatus = @file_get_contents('https://api.telegram.org/bot'. TOKEN .'/sendMessage?chat_id=' . CHATID . '&parse_mode=html&text=' . $txt); 
 
    if( isset(json_decode($textSendStatus)->{'ok'}) && json_decode($textSendStatus)->{'ok'} ) {
      if (!empty($_FILES['files']['tmp_name'])) {
     
          $urlFile =  "https://api.telegram.org/bot" . TOKEN . "/sendMediaGroup";
           
          // Путь загрузки файлов
          $path = $_SERVER['DOCUMENT_ROOT'] . '/telegramform/tmp/';
           
          // Загрузка файла и вывод сообщения
          $mediaData = [];
          $postContent = [
            'chat_id' => CHATID,
          ];
       
          for ($ct = 0; $ct < count($_FILES['files']['tmp_name']); $ct++) {
            if ($_FILES['files']['name'][$ct] && @copy($_FILES['files']['tmp_name'][$ct], $path . $_FILES['files']['name'][$ct])) {
              if ($_FILES['files']['size'][$ct] < $size && in_array($_FILES['files']['type'][$ct], $types)) {
                $filePath = $path . $_FILES['files']['name'][$ct];
                $postContent[$_FILES['files']['name'][$ct]] = new CURLFile(realpath($filePath));
                $mediaData[] = ['type' => 'document', 'media' => 'attach://'. $_FILES['files']['name'][$ct]];
              }
            }
          }
       
          $postContent['media'] = json_encode($mediaData);
       
          $curl = curl_init();
          curl_setopt($curl, CURLOPT_HTTPHEADER, ["Content-Type:multipart/form-data"]);
          curl_setopt($curl, CURLOPT_URL, $urlFile);
          curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
          curl_setopt($curl, CURLOPT_POSTFIELDS, $postContent);
          $fileSendStatus = curl_exec($curl);
          curl_close($curl);
          $files = glob($path.'*');
          foreach($files as $file){
            if(is_file($file))
              unlink($file);
          }
      }
      echo json_encode('SUCCESS');
    } else {
      echo json_encode('ERROR');
      // 
      // echo json_decode($textSendStatus);
    }
  } else {
    echo json_encode('NOTVALID');
  }
} else {
  header("Location: /");
}