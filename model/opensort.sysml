package OpenSort {
    private import ScalarValues::*;

    enum def StationExit {
        enum exit1;
        enum exit2;
        enum exit3;
        enum review;
    }

    item def PackageDetected;
    item def ResetRequested {
        doc /* Nueva pulsación tras inspeccionar y despejar la estación.
               No se conserva una solicitud rechazada ni una pulsación previa
               al bloqueo. Mantener pulsado no genera solicitudes adicionales. */
    }
    item def CycleConfirmed;
    item def CycleFailed;
    port def ResetSignal { out item request : ResetRequested; }

    item def QrResult {
        doc /* Una lectura válida entrega el ID del paquete. La ausencia de QR, un fallo de
               lectura o un timeout se trata como QR ilegible. */
        attribute readable : Boolean;
        attribute packageId : String [0..1];
    }
    item def DestinationQuery {
        attribute packageId : String;
    }
    enum def LookupStatus {
        enum found;
        enum unknownId;
        enum unavailable;
    }
    item def DestinationResult {
        attribute status : LookupStatus;
        attribute destination : String [0..1];
    }
    item def DivertOrder {
        attribute expectedExit : StationExit;
    }
    item def ExitObservation {
        attribute observedExit : StationExit;
    }

    port def EntrySignal { out item detected : PackageDetected; }
    port def QrSignal { out item result : QrResult; }
    port def ManifestAccess {
        out item query : DestinationQuery;
        in item result : DestinationResult;
    }
    port def DivertSignal { out item order : DivertOrder; }
    port def ExitSignal { out item observation : ExitObservation; }

    part def BenchStation {
        doc /* V1 admite un paquete por ciclo. Las conexiones representan
               intercambios lógicos. Quedan por definir pines, polaridad,
               filtrado, protocolo del lector, mando del desviador, ubicación
               del manifiesto y tiempos de lectura, posicionamiento y salida. */
        part entrySensor { port signal : EntrySignal; }
        part resetButton { port signal : ResetSignal; }
        part qrReader { port signal : QrSignal; }
        part manifestSource { port access : ~ManifestAccess; }
        part diverter { port signal : ~DivertSignal; }
        part exitSensors {
            doc /* Agrupa los sensores de las tres salidas y de revisión. */
            port signal : ExitSignal;
        }
        part controller {
            doc /* Controlador previsto: ESP32. */
            port reset : ~ResetSignal;
            exhibit state operatingStates : StationStates;
            port entry : ~EntrySignal;
            port qr : ~QrSignal;
            port manifest : ManifestAccess;
            port divert : DivertSignal;
            port exitObservation : ~ExitSignal;
        }

        connect resetButton.signal to controller.reset;
        connect entrySensor.signal to controller.entry;
        connect qrReader.signal to controller.qr;
        connect controller.manifest to manifestSource.access;
        connect controller.divert to diverter.signal;
        connect exitSensors.signal to controller.exitObservation;
    }

    action def PackageCycle {
        doc /* Flujo funcional de un intento. Los valores de decisión resumen
               los resultados de lectura, consulta y confirmación. La estación
               abre el ciclo al activarse el sensor de entrada estando libre. */
        in qrReadable : Boolean;
        in manifestAvailable : Boolean;
        in routeFound : Boolean;
        in exitMatches : Boolean;

        first start;
        then action detectPackage;
        then action readQr;
        then decide qrDecision;
            if qrReadable then queryManifest;
            else selectReview;

        action queryManifest;
        then decide manifestDecision;
            if manifestAvailable then checkRoute;
            else selectReview;

        action checkRoute {
            doc /* Se requiere un ID conocido y una ruta para su destino. */
        }
        then decide routeDecision;
            if routeFound then selectDestinationExit;
            else selectReview;

        action selectDestinationExit;
        then selectedExit;
        action selectReview {
            doc /* Sin QR, QR ilegible, manifiesto no encontrado o no disponible,
                   ID desconocido o destino sin ruta: enviar a revisión.
                   La salida de revisión también requiere confirmación física. */
        }
        then selectedExit;

        merge selectedExit;
        then action orderDiversion;
        then action awaitExit {
            doc /* La observación es independiente de la orden. El resultado
                   exitMatches es falso si se observa otra salida o vence el
                   plazo sin observación. También se confirma la salida de revisión. */
        }
        then decide exitDecision;
            if exitMatches then recordConfirmedExit;
            else blockAdmission;

        action recordConfirmedExit;
        then done;

        action blockAdmission {
            doc /* Registra la discrepancia o el timeout y bloquea la
                   admisión del siguiente paquete. El intento termina, pero la estación
                   permanece bloqueada hasta un rearme aceptado en StationStates. */
        }
        then done;

    }
    state def StationStates {
        doc /* Estados lógicos de operación; no representan la secuencia de arranque.
               PackageCycle produce CycleConfirmed al confirmar la salida y
               CycleFailed ante salida incorrecta o timeout.
               El adaptador del controlador entrega los eventos de entrada y rearme.
               Los valores de los sensores se muestrean al recibir cada solicitud.
               Su conexión detallada al hardware queda pendiente.
               Fuera de blocked, el rearme se ignora y no se almacena. */
        in attribute entrySensorClear : Boolean;
        in attribute exitSensorsClear : Boolean;

        entry; then available;

        state available;
        accept PackageDetected then processing;

        state processing;
        accept CycleConfirmed then available;
        accept CycleFailed then blocked;

        state blocked {
            doc /* Admisión deshabilitada. El operador inspecciona y retira
                   paquetes antes de pulsar. Sensores libres no demuestran
                   por sí solos que el espacio entre sensores esté vacío. */
        }
        accept ResetRequested
            if entrySensorClear and exitSensorsClear
            do action recordAcceptedReset {
                doc /* Registrar el rearme asociado al intento fallido,
                       conservar su resultado y habilitar la admisión.
                       No ordenar movimiento ni iniciar otro ciclo. */
            }
            then available;
        accept ResetRequested
            if not (entrySensorClear and exitSensorsClear)
            do action recordRejectedReset {
                doc /* Registrar rechazo y conservar bloqueo. Tras despejar
                       la estación se requiere una nueva pulsación. */
            }
            then blocked;
    }

}
